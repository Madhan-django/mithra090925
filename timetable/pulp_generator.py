import logging
from django.shortcuts import redirect
from django.contrib import messages
from pulp import LpProblem, LpVariable, LpMinimize, LpBinary, lpSum, LpStatus, PULP_CBC_CMD
from timetable.models import TeachingAllocation, TimeSlot, Timetable, ReservedSlot
from institutions.models import school
from setup.models import currentacademicyr, academicyr

logger = logging.getLogger(__name__)

# ------------------- Build Model -------------------
def build_model(allocations, timeslots, reserved_slots, allow_adaptive=False):
    model = LpProblem("School_Timetable", LpMinimize)

    # Binary variables for each allocation in each timeslot
    alloc_vars = {
        (a.id, ts.id): LpVariable(f"alloc_{a.id}_ts_{ts.id}", 0, 1, LpBinary)
        for a in allocations for ts in timeslots
    }

    adaptive_info = []
    problematic_allocations = []

    # 1️⃣ Subject weekly hours
    for a in allocations:
        model += (
            lpSum(alloc_vars[(a.id, ts.id)] for ts in timeslots) == a.hours_per_week,
            f"Hours_{a.id}"
        )

    # 2️⃣ No teacher overlap
    for ts in timeslots:
        for t_id in set(a.teacher_id for a in allocations):
            model += (
                lpSum(alloc_vars[(a.id, ts.id)] for a in allocations if a.teacher_id == t_id) <= 1,
                f"TeacherOverlap_{t_id}_{ts.id}"
            )

    # 3️⃣ No section overlap
    for ts in timeslots:
        for s_id in set(a.section_id for a in allocations):
            model += (
                lpSum(alloc_vars[(a.id, ts.id)] for a in allocations if a.section_id == s_id) <= 1,
                f"SectionOverlap_{s_id}_{ts.id}"
            )

    # 4️⃣ Class teacher first period (at least 3 days if possible)
    for alloc in allocations:
        if getattr(alloc, "is_classteacher", False):
            first_period_slots = [ts for ts in timeslots if ts.period_number == 1]
            required_first_periods = min(3, len(first_period_slots), alloc.hours_per_week)
            model += (
                lpSum(alloc_vars[(alloc.id, ts.id)] for ts in first_period_slots) >= required_first_periods,
                f"CT_{alloc.id}_Min3FirstPeriods"
            )

    # 5️⃣ Not first / not last period constraints
    for alloc in allocations:
        if getattr(alloc, "not_first", False):
            first_period_slots = [ts for ts in timeslots if ts.period_number == 1]
            for ts in first_period_slots:
                model += alloc_vars[(alloc.id, ts.id)] == 0, f"NotFirst_{alloc.id}_{ts.id}"

        if getattr(alloc, "not_last", False):
            max_period = max(ts.period_number for ts in timeslots)
            last_period_slots = [ts for ts in timeslots if ts.period_number == max_period]
            for ts in last_period_slots:
                model += alloc_vars[(alloc.id, ts.id)] == 0, f"NotLast_{alloc.id}_{ts.id}"

    # 6️⃣ Reserved slots
    counter = 0
    for r in reserved_slots:
        alloc = next(
            (a for a in allocations if a.section_id == r.section_id and a.subject_id == r.subject_id),
            None
        )
        if not alloc:
            continue

        counter += 1
        base_name = f"Res_{alloc.id}_{r.timeslot.id}_{counter}"

        # Strict reservation
        if not allow_adaptive or (not r.adaptive_day and not r.adaptive_period):
            model += alloc_vars[(alloc.id, r.timeslot.id)] == 1, f"{base_name}_Fixed"
            model += (
                lpSum(
                    alloc_vars[(a.id, r.timeslot.id)]
                    for a in allocations
                    if a.section_id == r.section_id and a.id != alloc.id
                ) == 0,
                f"{base_name}_Block",
            )
        else:
            # Adaptive reservation
            possible_slots = []
            if r.adaptive_day and r.adaptive_period:
                possible_slots = [ts for ts in timeslots]
            elif r.adaptive_day:
                possible_slots = [
                    ts for ts in timeslots if ts.period_number == r.timeslot.period_number
                ]
            elif r.adaptive_period:
                possible_slots = [ts for ts in timeslots if ts.day == r.timeslot.day]

            # Exclude other reserved slots of the same section
            occupied_ts_ids = [
                rr.timeslot.id for rr in reserved_slots if rr.section_id == r.section_id and rr != r
            ]
            possible_slots = [ts for ts in possible_slots if ts.id not in occupied_ts_ids]

            if not possible_slots:
                msg = f"No adaptive slot available for {r.subject.subject_name} (Section {r.section.section_name})"
                adaptive_info.append("⚠️ " + msg)
                problematic_allocations.append(msg)
                continue

            counter += 1
            cname = f"Adaptive_{alloc.id}_{r.timeslot.id}_{counter}"
            model += lpSum(alloc_vars[(alloc.id, ts.id)] for ts in possible_slots) == 1, cname

            adaptive_info.append(
                f"✅ Adaptive reservation for {r.subject.subject_name} "
                f"(Section {r.section.section_name}) possible slots: "
                f"{[f'{ts.day}-{ts.period_number}' for ts in possible_slots]}"
            )

    # 7️⃣ Teacher workload balance (per day)
    days = set(ts.day for ts in timeslots)
    for t_id in set(a.teacher_id for a in allocations):
        total_hours = sum(a.hours_per_week for a in allocations if a.teacher_id == t_id)
        ideal_max = (total_hours + len(days) - 1) // len(days)  # ceiling division
        for day in days:
            model += (
                lpSum(
                    alloc_vars[(a.id, ts.id)]
                    for a in allocations if a.teacher_id == t_id
                    for ts in timeslots if ts.day == day
                ) <= ideal_max,
                f"TeacherMax_{t_id}_{day}"
            )

    # 8️⃣ Soft constraint: penalise consecutive same-subject periods for a section
    #
    # For every section, subject, day — find pairs of timeslots whose
    # period_numbers are consecutive (p and p+1).  A binary penalty variable
    # "consec" is 1 when BOTH slots are assigned to the same allocation
    # (same subject, same section).  Consecutive periods across different
    # days are NOT penalised (they don't feel consecutive to students).
    #
    # Linearisation of  consec >= x_a_ts1 + x_a_ts2 - 1
    #   =>  consec >= x1 + x2 - 1   (consec is driven to 1 when both are 1)
    #   =>  consec <= x1             (can't be 1 if first slot isn't used)
    #   =>  consec <= x2             (can't be 1 if second slot isn't used)
    #
    # We then minimise the weighted sum of all consec variables.

    consec_vars = {}
    penalty_weight = 10   # tune higher to discourage more aggressively

    # Build a quick lookup: (day, period_number) -> TimeSlot
    ts_by_day_period = {}
    for ts in timeslots:
        ts_by_day_period[(ts.day, ts.period_number)] = ts

    consec_counter = 0
    for a in allocations:
        for ts in timeslots:
            next_ts = ts_by_day_period.get((ts.day, ts.period_number + 1))
            if next_ts is None:
                continue  # ts is the last period of the day

            consec_counter += 1
            cvar_name = f"Consec_{a.id}_{ts.id}_{next_ts.id}"
            cvar = LpVariable(cvar_name, 0, 1, LpBinary)
            consec_vars[(a.id, ts.id, next_ts.id)] = cvar

            x1 = alloc_vars[(a.id, ts.id)]
            x2 = alloc_vars[(a.id, next_ts.id)]

            # cvar >= x1 + x2 - 1  →  x1 + x2 - cvar <= 1
            model += (
                x1 + x2 - cvar <= 1,
                f"ConsecLB_{a.id}_{ts.id}_{next_ts.id}"
            )
            # cvar <= x1  and  cvar <= x2  (redundant but tighten LP relaxation)
            model += cvar <= x1, f"ConsecUB1_{a.id}_{ts.id}_{next_ts.id}"
            model += cvar <= x2, f"ConsecUB2_{a.id}_{ts.id}_{next_ts.id}"

    # Objective: minimise total consecutive same-subject periods (soft penalty)
    if consec_vars:
        model += penalty_weight * lpSum(consec_vars.values())
    else:
        model += 0

    return model, alloc_vars, adaptive_info, problematic_allocations


# ------------------- Generate Timetable -------------------
def generate_timetable_with_pulp(sch_id):
    try:
        sdata = school.objects.get(pk=sch_id)
        yr = currentacademicyr.objects.get(school_name=sdata)
        year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    except Exception as e:
        return f"❌ Error fetching school/academic year: {str(e)}", []

    allocations = list(
        TeachingAllocation.objects.filter(teacher_school=sdata).select_related(
            "teacher", "subject", "section"
        )
    )
    timeslots = list(TimeSlot.objects.filter(period_school=sdata))
    reserved_slots = list(ReservedSlot.objects.filter(school=sdata))

    # Try strict reservation mode first
    model, alloc_vars, adaptive_info, problematic_allocations = build_model(
        allocations, timeslots, reserved_slots, allow_adaptive=False
    )
    status = model.solve(PULP_CBC_CMD(msg=0))

    # Retry with adaptive mode if strict fails
    if LpStatus[status] != "Optimal":
        model, alloc_vars, adaptive_info, problematic_allocations = build_model(
            allocations, timeslots, reserved_slots, allow_adaptive=True
        )
        status = model.solve(PULP_CBC_CMD(msg=0))

    for msg in adaptive_info:
        logger.info(msg)

    if LpStatus[status] != "Optimal":
        return (
            f"❌ Timetable could not be generated even with adaptive reservations. Problems:\n"
            + "\n".join(problematic_allocations),
            problematic_allocations,
        )

    # Save generated timetable
    Timetable.objects.filter(timetable_school=sdata).delete()
    for a in allocations:
        for ts in timeslots:
            val = alloc_vars[(a.id, ts.id)].value()
            if val is not None and val >= 0.99:
                Timetable.objects.create(
                    section=a.section,
                    subject=a.subject,
                    teacher=a.teacher,
                    timeslot=ts,
                    timetable_school=sdata,
                )

    return "✅ Timetable generated successfully with all constraints!", []

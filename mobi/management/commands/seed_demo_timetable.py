from django.core.management.base import BaseCommand
from datetime import date, time, timedelta


class Command(BaseCommand):
    help = 'Seed class timetable and exam timetable for Demo School II-A'

    def handle(self, *args, **options):
        from institutions.models import school
        from admission.models import students
        from setup.models import sclass, section, subjects, academicyr, currentacademicyr
        from staff.models import staff
        from timetable.models import TimeSlot, Timetable, TeachingAllocation
        from examination.models import (
            exam_group, exams, exam_subjectmap, admit_card, exam_result
        )

        demo  = school.objects.get(pk=4)
        cls   = sclass.objects.get(pk=33)    # II-Standard
        sec   = section.objects.get(pk=58)   # II-A
        yr    = currentacademicyr.objects.get(school_name=demo)
        year  = academicyr.objects.get(acad_year=yr, school_name=demo)
        teacher = staff.objects.get(pk=10)   # admin staff

        ii_a_students = students.objects.filter(class_name=cls, secs=sec)

        self.stdout.write('Seeding timetable data for Demo School II-A...')

        # ── 1. Add subjects ─────────────────────────────────────────────────
        subject_data = [
            ('English',  'E1002'),
            ('Maths',    'M1003'),
            ('Science',  'Sc1004'),
            ('Social',   'So1005'),
        ]
        subject_objs = {}
        tamil = subjects.objects.get(pk=435)
        subject_objs['Tamil'] = tamil

        for sname, scode in subject_data:
            subj, created = subjects.objects.get_or_create(
                subject_name  = sname,
                subject_class = cls,
                subject_year  = year,
                subject_school= demo,
                defaults={'subject_code': scode},
            )
            subject_objs[sname] = subj
            if created:
                self.stdout.write(f'  [OK] Subject created: {sname}')
            else:
                self.stdout.write(f'  - Subject already exists: {sname}')

        all_subs = list(subject_objs.values())  # [Tamil, English, Maths, Science, Social]

        # ── 2. TimeSlots (Mon-Fri, 5 periods) ───────────────────────────────
        if TimeSlot.objects.filter(period_school=demo).count() == 0:
            days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
            for day in days:
                for period in range(1, 6):
                    TimeSlot.objects.create(
                        day=day, period_number=period, period_school=demo
                    )
            self.stdout.write('  [OK] 25 TimeSlots created (Mon-Fri, 5 periods)')
        else:
            self.stdout.write('  - TimeSlots already exist, skipped')

        # ── 3. TeachingAllocation for II-A ───────────────────────────────────
        for subj in all_subs:
            TeachingAllocation.objects.get_or_create(
                teacher=teacher, subject=subj, cls=cls, section=sec,
                teacher_school=demo,
                defaults={'hours_per_week': 5},
            )
        self.stdout.write('  [OK] TeachingAllocation set for all 5 subjects')

        # ── 4. Timetable entries for II-A ─────────────────────────────────
        if Timetable.objects.filter(section=sec, timetable_school=demo).count() == 0:
            # Layout: day -> [p1, p2, p3, p4, p5] (subject names)
            layout = {
                'Mon': ['Tamil',   'English', 'Maths',   'Science', 'Social'],
                'Tue': ['English', 'Tamil',   'Science', 'Maths',   'Social'],
                'Wed': ['Maths',   'Science', 'Tamil',   'English', 'Social'],
                'Thu': ['Social',  'Maths',   'English', 'Tamil',   'Science'],
                'Fri': ['Science', 'Social',  'Maths',   'English', 'Tamil'],
            }
            entries = []
            for day, periods in layout.items():
                for period_no, sname in enumerate(periods, start=1):
                    slot = TimeSlot.objects.get(
                        day=day, period_number=period_no, period_school=demo
                    )
                    entries.append(Timetable(
                        section=sec,
                        subject=subject_objs[sname],
                        teacher=teacher,
                        timeslot=slot,
                        timetable_school=demo,
                    ))
            Timetable.objects.bulk_create(entries)
            self.stdout.write(f'  [OK] {len(entries)} Timetable entries created for II-A')
        else:
            self.stdout.write('  - Timetable entries already exist, skipped')

        # ── 5. Exam timetable — add more subjects to existing exam ───────────
        exam = exams.objects.get(exam_school=demo, exam_class=cls)
        existing_maps = exam_subjectmap.objects.filter(exname=exam).values_list('exam_subjects_id', flat=True)

        exam_schedule = [
            ('English', date(2026, 10, 6),  time(9, 0), time(12, 0), 'Room 101'),
            ('Maths',   date(2026, 10, 7),  time(9, 0), time(12, 0), 'Room 102'),
            ('Science', date(2026, 10, 8),  time(9, 0), time(12, 0), 'Room 101'),
            ('Social',  date(2026, 10, 9),  time(9, 0), time(12, 0), 'Room 102'),
        ]
        new_maps = []
        for sname, pdate, stime, etime, room in exam_schedule:
            subj = subject_objs[sname]
            if subj.id not in existing_maps:
                sm = exam_subjectmap.objects.create(
                    exname=exam,
                    exam_subjects=subj,
                    exam_subject_type='Theory',
                    paper_code=f'{sname[:3].upper()}1',
                    paper_date=pdate,
                    start_time=stime,
                    end_time=etime,
                    room_no=room,
                    max_marks=100,
                )
                new_maps.append(sm)
                self.stdout.write(f'  [OK] Exam paper added: {sname} on {pdate}')
        if not new_maps:
            self.stdout.write('  - Exam subject maps already exist, skipped')

        # Update exam Sub_count
        total_maps = exam_subjectmap.objects.filter(exname=exam).count()
        exam.exam_Sub_count = total_maps
        exam.save()

        # ── 6. Admit cards for all II-A students ────────────────────────────
        all_submaps = list(exam_subjectmap.objects.filter(exname=exam))
        created_count = 0
        for stud in ii_a_students:
            ac, created = admit_card.objects.get_or_create(
                exam_stu=stud,
                exam_label=exam,
                defaults={'examno': f'D{stud.id:04d}'},
            )
            if created:
                created_count += 1
                # Add sample exam results for each subject
                for sm in all_submaps:
                    if not exam_result.objects.filter(adm_card=ac, exam_sub=sm).exists():
                        exam_result.objects.create(
                            obtained_marks=70 + (stud.id % 25),
                            exam_sub=sm,
                            adm_card=ac,
                            remark='',
                        )
        if created_count:
            self.stdout.write(f'  [OK] {created_count} Admit cards created for II-A students')
        else:
            self.stdout.write('  - Admit cards already exist for all II-A students')

        self.stdout.write(self.style.SUCCESS('\nDone! Test endpoints:'))
        self.stdout.write('  GET mobi/exam_timetable/?username=9047621499')
        self.stdout.write('  GET mobi/timetable/?username=9047621499')
        self.stdout.write('  GET mobi/ResultDownload/?username=9047621499')

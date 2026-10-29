from staff.models import temp_homework, homework
from django.http import HttpResponse
from institutions.models import school
from django.utils import timezone
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


def send_homework(sch_id):
    sch_id = sch_id[0]

    sdata = school.objects.get(id=sch_id)
    today = timezone.localdate()

    cpy = temp_homework.objects.filter(
        school_homework=sdata,
        homework_date=today
    )

    homework_list = [
        homework(
            title=data.title,
            hclass=data.hclass,
            secs=data.secs,
            subj=data.subj,
            homework_date=data.homework_date,
            description=data.description,
            submission_date=data.submission_date,
            created_by=data.created_by,
            acad_yr=data.acad_yr,
            school_homework=data.school_homework,
            attachment=data.attachment
        )
        for data in cpy
    ]

    homework.objects.bulk_create(homework_list)
    return len(homework_list)


def sync_homework_all_schools():
    """Daily 2AM task: copy today's temp_homework → homework for every school."""
    today = timezone.localdate()
    all_schools = school.objects.all()
    total = 0

    for sdata in all_schools:
        cpy = temp_homework.objects.filter(school_homework=sdata, homework_date=today)
        if not cpy.exists():
            continue

        # Avoid duplicates if the task fires more than once on the same day
        existing_keys = set(
            homework.objects.filter(school_homework=sdata, homework_date=today)
            .values_list('hclass_id', 'secs_id', 'subj_id', 'created_by_id')
        )

        to_create = [
            homework(
                title=data.title,
                hclass=data.hclass,
                secs=data.secs,
                subj=data.subj,
                homework_date=data.homework_date,
                description=data.description,
                submission_date=data.submission_date,
                created_by=data.created_by,
                acad_yr=data.acad_yr,
                school_homework=data.school_homework,
                attachment=data.attachment,
            )
            for data in cpy
            if (data.hclass_id, data.secs_id, data.subj_id, data.created_by_id) not in existing_keys
        ]

        if to_create:
            homework.objects.bulk_create(to_create)
            total += len(to_create)

    logger.info("sync_homework_all_schools: copied %d records for %s", total, today)
    return f"Copied {total} homework(s) for {today}"



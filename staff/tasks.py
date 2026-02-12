from staff.models import temp_homework,homework
from django.http import HttpResponse
from institutions.models import school
from django.utils import timezone
from datetime import datetime, timedelta


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



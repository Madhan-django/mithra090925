from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, time, timedelta
import random

class Command(BaseCommand):
    help = 'Seed Demo School (pk=4) with data to test every mobile API endpoint'

    def handle(self, *args, **options):
        from institutions.models import school
        from admission.models import students
        from setup.models import academicyr, currentacademicyr
        from mobi.models import SchoolProfile, Banner
        from academic.models import noticeboard, events
        from mobiplayer.models import Video
        from students.models import attendance
        from fees.models import fees, addindfee
        from examination.models import (
            exam_group, exams, exam_subjectmap, admit_card, exam_result
        )
        from setup.models import subjects

        demo = school.objects.get(pk=4)
        stud = students.objects.get(usernm='9047621499')
        yr = currentacademicyr.objects.get(school_name=demo)
        year = academicyr.objects.get(acad_year=yr, school_name=demo)
        cls = stud.class_name
        sec = stud.secs

        self.stdout.write('Seeding Demo School data...')

        # ── 1. School web URLs ──────────────────────────────────────────────
        demo.web_aboutus   = 'https://mithran.co.in/about'
        demo.web_contactus = 'https://mithran.co.in/contact'
        demo.web_gallery   = 'https://mithran.co.in/gallery'
        demo.web_admission = 'https://mithran.co.in/admission'
        demo.website       = 'https://mithran.co.in'
        demo.save()
        self.stdout.write('  [OK] School web URLs updated')

        # ── 2. SchoolProfile ────────────────────────────────────────────────
        if not SchoolProfile.objects.filter(school_name=demo).exists():
            SchoolProfile.objects.create(
                school_name   = demo,
                tagline       = 'Excellence in Education',
                about         = 'Demo School is a premier institution dedicated to holistic student development.',
                logo          = 'logos/demo_logo.png',
                founder_name  = 'Dr. A. Demo',
                founded_year  = '2005',
                city          = 'Chennai',
                phone         = '9876543210',
                email         = 'demo@mithran.co.in',
                address       = '123 Demo Street, Chennai - 600001',
                admission_open= True,
                admission_url = 'https://mithran.co.in/admission',
                gallery_url   = 'https://mithran.co.in/gallery',
            )
            self.stdout.write('  [OK] SchoolProfile created')
        else:
            self.stdout.write('  - SchoolProfile already exists, skipped')

        # ── 3. Noticeboard ──────────────────────────────────────────────────
        if noticeboard.objects.filter(notice_school=demo).count() == 0:
            notices = [
                ('Annual Day Celebration', 'Annual Day will be celebrated on 15th Oct. All students must attend.'),
                ('Exam Schedule Released', 'Term 1 exam schedule has been published. Check the timetable section.'),
                ('Holiday Notice', 'School will remain closed on 2nd Oct for Gandhi Jayanti.'),
            ]
            for title, content in notices:
                noticeboard.objects.create(
                    title         = title,
                    content       = content,
                    notice_date   = date.today() - timedelta(days=random.randint(1, 10)),
                    status        = 'Active',
                    notice_school = demo,
                )
            self.stdout.write('  [OK] 3 Noticeboard entries created')
        else:
            self.stdout.write('  - Noticeboard entries already exist, skipped')

        # ── 4. Events ───────────────────────────────────────────────────────
        if events.objects.filter(event_school=demo).count() == 0:
            evt_data = [
                ('Sports Day', 'Inter-house sports competition', 'School Ground'),
                ('Science Exhibition', 'Annual science fair for all classes', 'Main Hall'),
                ('Parent-Teacher Meeting', 'Term 1 PTM for all classes', 'Classrooms'),
            ]
            for title, desc, loc in evt_data:
                start = date.today() + timedelta(days=random.randint(5, 30))
                events.objects.create(
                    event_title    = title,
                    event_desc     = desc,
                    event_location = loc,
                    post_date      = date.today(),
                    start_date     = start,
                    end_date       = start + timedelta(days=1),
                    event_school   = demo,
                )
            self.stdout.write('  [OK] 3 Events created')
        else:
            self.stdout.write('  - Events already exist, skipped')

        # ── 5. Videos ───────────────────────────────────────────────────────
        if Video.objects.filter(Vschool=demo).count() == 0:
            videos_data = [
                ('School Tour 2024', 'A virtual tour of our school campus', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'),
                ('Annual Day Highlights', 'Best moments from Annual Day 2024', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'),
            ]
            for title, desc, link in videos_data:
                Video.objects.create(
                    VTitle    = title,
                    Vdesc     = desc,
                    Vlink     = link,
                    Vdate     = date.today(),
                    Vpostdate = date.today(),
                    status    = 'Active',
                    Vschool   = demo,
                )
            self.stdout.write('  [OK] 2 Videos created')
        else:
            self.stdout.write('  - Videos already exist, skipped')

        # ── 6. Attendance (3 months for test student) ───────────────────────
        if attendance.objects.filter(student_name=stud).count() == 0:
            today = date.today()
            att_records = []
            for month_offset in range(3):
                month_start = date(today.year, today.month, 1) - timedelta(days=30 * month_offset)
                for day in range(1, 26):
                    try:
                        att_date = date(month_start.year, month_start.month, day)
                    except ValueError:
                        break
                    if att_date.weekday() < 5:  # Mon–Fri only
                        status = 'Absent' if day in [5, 12, 19] else 'Present'
                        att_records.append(attendance(
                            student_name = stud,
                            attndate     = att_date,
                            aclass       = cls,
                            sec          = sec,
                            status       = status,
                        ))
            attendance.objects.bulk_create(att_records, ignore_conflicts=True)
            self.stdout.write(f'  [OK] {len(att_records)} Attendance records created (3 months)')
        else:
            self.stdout.write('  - Attendance records already exist, skipped')

        # ── 7. Fees ─────────────────────────────────────────────────────────
        if addindfee.objects.filter(stud_name=stud).count() == 0:
            fee_cats_data = [
                ('Term 1 Fees', 'First term tuition fee', 5000),
                ('Term 2 Fees', 'Second term tuition fee', 5000),
                ('Annual Fee',  'Annual maintenance fee', 2000),
            ]
            for i, (title, desc, amount) in enumerate(fee_cats_data):
                fee_cat = fees.objects.create(
                    invoice_title = title,
                    desc          = desc,
                    iclass        = cls,
                    issued_date   = date.today(),
                    due_date      = date.today() + timedelta(days=30),
                    fees_school   = demo,
                    fee_amount    = amount,
                    ac_year       = year,
                    latefee       = 0,
                    isactive      = 'yes',
                )
                addindfee.objects.create(
                    fee_cat    = fee_cat,
                    class_name = cls,
                    stud_name  = stud,
                    due_amt    = amount,
                    concession = 0,
                    invoice_no = 1000 + i,
                    status     = 'Paid' if i == 0 else 'Unpaid',
                )
            self.stdout.write('  [OK] 3 Fee records created (1 Paid, 2 Unpaid)')
        else:
            self.stdout.write('  - Fee records already exist, skipped')

        # ── 8. Exams + Timetable + Admit Card + Result ──────────────────────
        if exams.objects.filter(exam_school=demo).count() == 0:
            subj = subjects.objects.filter(subject_class=cls).first()
            if not subj:
                self.stdout.write('  [!] No subjects found for class — skipping exam seed')
            else:
                eg = exam_group.objects.create(
                    exm_group        = 'Term Exams',
                    exam_group_school= demo,
                )

                exam1 = exams.objects.create(
                    exam_title      = 'Term 1 Examination',
                    exam_code       = 'T1-2024',
                    exam_centre     = 'Main Block',
                    exam_class      = cls,
                    exam_Sub_count  = 1,
                    exam_start_date = date.today() + timedelta(days=10),
                    exam_end_date   = date.today() + timedelta(days=15),
                    exam_year       = year,
                    exam_school     = demo,
                    published       = 'Yes',
                    remark          = 'Term1',
                    exm_grp         = eg,
                )

                submap = exam_subjectmap.objects.create(
                    exname            = exam1,
                    exam_subjects     = subj,
                    exam_subject_type = 'Theory',
                    paper_code        = 'T1-TAM',
                    paper_date        = date.today() + timedelta(days=10),
                    start_time        = time(9, 0),
                    end_time          = time(12, 0),
                    room_no           = 'Room 101',
                    max_marks         = 100,
                )

                ac = admit_card.objects.create(
                    examno     = 'DEMO001',
                    exam_stu   = stud,
                    exam_label = exam1,
                )

                exam_result.objects.create(
                    obtained_marks = 78,
                    exam_sub       = submap,
                    adm_card       = ac,
                    remark         = 'Good',
                )

                self.stdout.write('  [OK] Exam group + Exam + SubjectMap + AdmitCard + Result created')
        else:
            self.stdout.write('  - Exams already exist, skipped')

        self.stdout.write(self.style.SUCCESS('\nAll done! Test with username: 9047621499'))
        self.stdout.write('Endpoints to verify:')
        endpoints = [
            'POST  mobi/api/token/',
            'GET   mobi/?username=9047621499',
            'GET   mobi/SchoolProfile/?username=9047621499',
            'GET   mobi/school/?username=9047621499',
            'GET   mobi/noticeboard/?username=9047621499',
            'GET   mobi/homework/?username=9047621499',
            'GET   mobi/fee/?username=9047621499',
            'GET   mobi/attendance/?username=9047621499',
            'GET   mobi/CalendarAbsentees/?username=9047621499',
            'GET   mobi/school_events/?username=9047621499',
            'GET   mobi/messages/?username=9047621499',
            'GET   mobi/videos/?username=9047621499',
            'GET   mobi/banners/?username=9047621499',
            'GET   mobi/exam_timetable/?username=9047621499',
            'GET   mobi/ResultDownload/?username=9047621499',
            'GET   mobi/grievance/?username=9047621499',
            'POST  mobi/grievance/?username=9047621499',
            'POST  mobi/FcmSave/?username=9047621499',
        ]
        for ep in endpoints:
            self.stdout.write(f'  {ep}')

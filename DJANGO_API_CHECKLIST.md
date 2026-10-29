# Mithra Mobile App — Django API Checklist

Use this file to verify every endpoint and field the Android app depends on exists in the Django backend.
Each section shows the HTTP method, path, auth, query params, and the exact JSON fields the app parses.

---

## Base URLs

| Variable      | Production value                    | Used for                              |
|---------------|-------------------------------------|---------------------------------------|
| `loginurl`    | `https://mithran.co.in/mobi/api/`   | JWT token login                       |
| `homeurl`     | `https://mithran.co.in/`            | Student profile, School profile       |
| `baseurl`     | `https://mithran.co.in/mobi/`       | All other APIs                        |

> All authenticated endpoints expect `Authorization: Bearer <access_token>` header
> and `?username=<student_username>` as a query parameter (except Login).

---

## 1. Authentication

### POST `{loginurl}token/`
Login and obtain JWT access token.

**Request body (JSON):**
```json
{
  "username": "string",
  "password": "string",
  "access": ""
}
```

**Response (JSON):**
```json
{
  "username": "string",
  "password": "string",
  "access": "eyJ..."
}
```
> The app stores `access` as the Bearer token. `username` and `password` are saved for token refresh.

---

## 2. Student Profile

### GET `{homeurl}mobi/`
**Auth:** Bearer token | **Query:** `?username=`

**Response — single object:**
```json
{
  "first_name": "string",
  "last_name": "string",
  "roll_no": "string",
  "student_photo": "/media/...",      // relative path, prepend homeurl
  "address": "string",
  "admn_date": "YYYY-MM-DD",
  "admn_no": 1,
  "blood_group": "string",
  "caste": "string",
  "dob_date": "YYYY-MM-DD",
  "email": "string",
  "father_name": "string",
  "father_occupation": "string",
  "gender": "string",
  "id": 1,
  "ac_year": 1,
  "account": null,
  "mother_name": "string",
  "mother_occupation": "string",
  "phone": "string",
  "religion": "string",
  "student_status": "string",
  "tc_date": null,
  "usernm": "string",
  "attendance_percentage": 90.5,      // nullable Double — used on Home dashboard
  "homewk": 3,                        // nullable Int — pending homework count
  "fee_status": "Paid",               // nullable String — "Paid" / "Unpaid" / other
  "class_name": {
    "id": 1,
    "name": "Class X",
    "acad_year": 1,
    "school_name": 1
  },
  "secs": {
    "section_name": "A"
  },
  "school_student": {
    "name": "School Name",
    "logo": "/media/..."              // nullable, relative path
  }
}
```
> Fields `attendance_percentage`, `homewk`, `fee_status` are **newly required** — used on the Home dashboard badges.
> `school_student.logo` is used to update the school logo cached in SharedPreferences.

---

## 3. School Profile (About Us / My Profile screens)

### GET `{homeurl}mobi/SchoolProfile/`
**Auth:** Bearer token | **Query:** `?username=`

**Response — single object:**
```json
{
  "id": 1,
  "tagline": "string",
  "about": "string",
  "logo": "/media/...",
  "founder_name": "string",
  "founder_pic": "/media/...",
  "founded_year": "2000",
  "city": "string",
  "phone": "string",
  "email": "string",
  "address": "string",
  "admission_open": true,
  "admission_url": "https://...",
  "gallery_url": "https://...",
  "school_name": {
    "id": 1,
    "name": "string"
  }
}
```
> All fields are nullable in the model. Return `null` for missing fields rather than omitting them.

---

## 4. School Info (About Us screen)

### GET `{baseurl}school/`
**Auth:** Bearer token | **Query:** `?username=`

**Response — single object:**
```json
{
  "id": 1,
  "name": "School Name",
  "address": "string",
  "email": "string",
  "phone": "string",
  "regno": "string",
  "logo": "/media/...",
  "isactive": true,
  "website": "https://...",
  "web_gallery": "https://...",
  "web_contactus": "https://...",
  "web_aboutus": "https://...",
  "web_admission": "https://..."
}
```
> `website`, `web_gallery`, `web_contactus`, `web_aboutus`, `web_admission` are **newly required** fields.
> App opens these as URLs in the browser from the About Us screen.

---

## 5. Noticeboard

### GET `{baseurl}noticeboard/`
**Auth:** Bearer token | **Query:** `?username=`

**Response — list:**
```json
[
  {
    "id": 1,
    "title": "string",
    "content": "string",
    "file": "/media/...",
    "url": "https://...",
    "notice_date": "YYYY-MM-DD",
    "status": "string",
    "notice_school": {
      "id": 1,
      "name": "string",
      "address": "string",
      "email": "string",
      "phone": "string",
      "logo": "/media/...",
      "regno": "string",
      "isactive": true
    }
  }
]
```
> App shows top 3 items as a preview on the Home dashboard (`title` + `notice_date`).

---

## 6. Homework

### GET `{baseurl}homework/`
**Auth:** Bearer token | **Query:** `?username=`

**Response — list:**
```json
[
  {
    "id": 1,
    "title": "string",
    "description": "string",
    "homework_date": "YYYY-MM-DD",
    "submission_date": "YYYY-MM-DD",
    "attachment": "/media/...",       // nullable
    "acad_yr": 1,
    "school_homework": 1,
    "subj": {
      "id": 1,
      "subject_name": "string",
      "subject_code": "string",
      "subject_class": 1,
      "subject_school": 1,
      "subject_year": 1
    },
    "hclass": {
      "id": 1,
      "name": "string",
      "acad_year": 1,
      "school_name": 1
    },
    "secs": {
      "id": 1,
      "section_name": "string",
      "acad_year": 1,
      "class_sec_name": 1,
      "school_name": 1
    },
    "created_by": {
      "id": 1,
      "first_name": "string",
      "last_name": "string",
      "email": "string",
      "mobile": "string",
      "desg": "string",
      "role": "string",
      "gender": "string",
      "dob": "YYYY-MM-DD",
      "join": "YYYY-MM-DD",
      "address": "string",
      "desc": "string",
      "certifications": "string",
      "experience": "string",
      "qualification": "string",
      "permission_group": "string",
      "salary": 0.0,
      "status": "string",
      "staff_photo": null,
      "staff_school": 1,
      "staff_user": 1,
      "subjects_taught": [1, 2]
    }
  }
]
```

---

## 7. Fee

### GET `{baseurl}fee/`
**Auth:** Bearer token | **Query:** `?username=`

**Response — list:**
```json
[
  {
    "id": 1,
    "concession": 0,
    "due_amt": 5000,
    "status": "Paid",
    "invoice_no": 101,
    "class_name": {
      "id": 1,
      "name": "string",
      "acad_year": 1,
      "school_name": 1
    },
    "fee_cat": {
      "id": 1,
      "invoice_title": "string",
      "desc": "string",
      "fee_amount": 5000,
      "latefee": 0,
      "due_date": "YYYY-MM-DD",
      "issued_date": "YYYY-MM-DD",
      "isactive": "string",
      "fee_group": null,
      "iclass": { "id": 1, "name": "string", "acad_year": 1, "school_name": 1 },
      "ac_year": { "id": 1, "acad_year": "2024-25", "school_name": 1 },
      "fees_school": {
        "id": 1, "name": "string", "address": "string", "email": "string",
        "phone": "string", "logo": "/media/...", "regno": "string", "isactive": true
      }
    },
    "stud_name": { /* full StudentClass object — same as /mobi/ response */ }
  }
]
```

---

## 8. Attendance (Monthly Summary)

### GET `{baseurl}attendance/`
**Auth:** Bearer token | **Query:** `?username=`

**Response — list (one item per month):**
```json
[
  {
    "month": "January",
    "attendance_data": 22,
    "absent": 3
  }
]
```

---

## 9. Attendance Calendar (Daily)

### GET `{baseurl}CalendarAbsentees/`
**Auth:** Bearer token | **Query:** `?username=`

**Response — list (absent days only):**
```json
[
  {
    "id": 1,
    "attndate": "YYYY-MM-DD",
    "status": "Absent",
    "aclass": 1,
    "sec": 1,
    "student_name": {
      "id": 1,
      "first_name": "string",
      "last_name": "string",
      "roll_no": "string",
      "usernm": "string",
      "student_photo": "/media/...",
      "address": "string",
      "admn_date": "YYYY-MM-DD",
      "admn_no": 1,
      "blood_group": "string",
      "caste": "string",
      "dob_date": "YYYY-MM-DD",
      "email": "string",
      "father_name": "string",
      "father_occupation": "string",
      "gender": "string",
      "ac_year": 1,
      "account": null,
      "mother_name": "string",
      "mother_occupation": "string",
      "phone": "string",
      "religion": "string",
      "student_status": "string",
      "tc_date": null,
      "class_name": { "id": 1, "name": "string", "acad_year": 1, "school_name": 1 },
      "secs": { "id": 1, "section_name": "string", "acad_year": 1, "class_sec_name": 1, "school_name": 1 },
      "school_student": { "id": 1, "name": "string", "logo": "/media/..." }
    }
  }
]
```

---

## 10. Events

### GET `{baseurl}school_events/`
**Auth:** Bearer token | **Query:** `?username=`

**Response — list:**
```json
[
  {
    "id": 1,
    "event_title": "string",
    "event_desc": "string",
    "event_location": "string",
    "event_image": null,
    "post_date": "YYYY-MM-DD",
    "start_date": "YYYY-MM-DD",
    "end_date": "YYYY-MM-DD",
    "event_school": {
      "id": 1, "name": "string", "address": "string", "email": "string",
      "phone": "string", "logo": "/media/...", "regno": "string", "isactive": true
    }
  }
]
```
> App counts total events vs last-seen count to show a badge on Home dashboard.

---

## 11. Messages / General Notifications

### GET `{baseurl}messages/`
**Auth:** Bearer token | **Query:** `?username=`

**Response — list:**
```json
[
  {
    "title": "string",
    "message": "string",
    "create_date": "YYYY-MM-DD"
  }
]
```
> App counts items to show a notification dot on the Home bell icon.

---

## 12. Video Gallery

### GET `{baseurl}videos/`
**Auth:** Bearer token | **Query:** `?username=`

**Response — list:**
```json
[
  {
    "id": 1,
    "VTitle": "string",
    "VThumbnail": "/media/...",
    "Vdesc": "string",
    "Vlink": "https://youtube.com/...",
    "Vdate": "YYYY-MM-DD",
    "Vpostdate": "YYYY-MM-DD",
    "status": "string",
    "Vschool": {
      "id": 1, "name": "string", "address": "string", "email": "string",
      "phone": "string", "logo": "/media/...", "regno": "string", "isactive": true
    }
  }
]
```
> `Vlink` is used as YouTube URL — opened in a WebView or YouTube player.

---

## 13. Banners (Home Slideshow)

### GET `{baseurl}banners/`
**Auth:** Bearer token | **Query:** `?username=`

**Response — list:**
```json
[
  {
    "id": 1,
    "title": "string",
    "image": "/media/...",
    "link_url": "https://...",
    "display_order": 1
  }
]
```
> **This is a newly added endpoint.** The Home dashboard shows a banner slideshow.
> `image` is a relative path — app prepends `homeurl`. `display_order` sorts the items.

---

## 14. Exam Timetable

### GET `{baseurl}exam_timetable/`
**Auth:** Bearer token | **Query:** `?username=`

**Response — list:**
```json
[
  {
    "paper_date": "YYYY-MM-DD",
    "start_time": "HH:MM:SS",
    "end_time": "HH:MM:SS",
    "room_no": "string",
    "exam_subjects": {
      "id": 1,
      "subject_name": "string",
      "subject_code": "string",
      "subject_class": 1,
      "subject_school": 1,
      "subject_year": 1
    },
    "exname": {
      "id": 1,
      "exam_title": "string",
      "exam_code": "string",
      "exam_start_date": "YYYY-MM-DD",
      "exam_end_date": "YYYY-MM-DD",
      "exam_centre": "string",
      "exam_class": 1,
      "exam_school": 1,
      "exam_year": 1,
      "published": "string",
      "remark": "string",
      "exam_Sub_count": 5,
      "exam_groupby": "string",
      "exm_grp": 1
    }
  }
]
```

---

## 15. Grievance

### GET `{baseurl}grievance/`
**Auth:** Bearer token | **Query:** `?username=`

**Response — list:**
```json
[
  {
    "id": 1,
    "area_of_complaint": "string",
    "aoc_other": null,
    "detail": "string",
    "mobile": "string",
    "complaint_date": "YYYY-MM-DD",
    "complaint_status": "string",
    "action_date": null,
    "principal_remark": null,
    "concern_person_remark": null,
    "act_details": null,
    "concern_person_name": "string",
    "no_action_taken": false
  }
]
```

### POST `{baseurl}grievance/`
**Auth:** Bearer token | **Query:** `?username=`

**Request body (JSON):**
```json
{
  "area_of_complaint": "string",
  "aoc_other": null,
  "detail": "string",
  "mobile": "string"
}
```
**Response:** Same as a single `GrievanceItem` above.

---

## 16. FCM Token Registration

### POST `{baseurl}FcmSave/`
**Auth:** Bearer token | **Query:** `?username=`

**Request body (JSON):**
```json
{
  "firecmToken": "string"
}
```
**Response:**
```json
{
  "firecmToken": "string"
}
```
> Called after login to register the device's Firebase Cloud Messaging token for push notifications.

---

## 17. Result PDF Download

### GET `{baseurl}ResultDownload/`
**Auth:** Bearer token | **Query:** `?username=`

**Response:** Raw binary (PDF file stream) — `Content-Type: application/pdf`

> App saves the PDF to the device using MediaStore (API 29+) or FileOutputStream (older).
> Uses 60-second timeout (separate OkHttp client).

---

## 18. Class Timetable

### GET `{baseurl}timetable/`
**Auth:** Bearer token | **Query:** `?username=`

**Response — list (ordered by day, then period):**
```json
[
  {
    "day": "Mon",
    "period_number": 1,
    "subject_name": "Tamil",
    "subject_code": "T1001",
    "teacher_name": "Admin Admin"
  },
  {
    "day": "Mon",
    "period_number": 2,
    "subject_name": "English",
    "subject_code": "E1002",
    "teacher_name": "Admin Admin"
  }
]
```
> Returns the weekly class timetable for the student's section.
> Days are short codes: `Mon`, `Tue`, `Wed`, `Thu`, `Fri`, `Sat`.
> `period_number` starts at 1. Items are ordered by day then period.

---

## Summary Checklist

| # | Endpoint                        | Method | New / Existing | Key new fields                                     |
|---|---------------------------------|--------|----------------|----------------------------------------------------|
| 1 | `{loginurl}token/`              | POST   | Existing       | —                                                  |
| 2 | `{homeurl}mobi/`                | GET    | Existing       | `attendance_percentage`, `homewk`, `fee_status`, `school_student.logo` |
| 3 | `{homeurl}mobi/SchoolProfile/`  | GET    | Existing       | All fields (check nullable)                        |
| 4 | `{baseurl}school/`              | GET    | Existing       | `website`, `web_gallery`, `web_contactus`, `web_aboutus`, `web_admission` |
| 5 | `{baseurl}noticeboard/`         | GET    | Existing       | —                                                  |
| 6 | `{baseurl}homework/`            | GET    | Existing       | —                                                  |
| 7 | `{baseurl}fee/`                 | GET    | Existing       | —                                                  |
| 8 | `{baseurl}attendance/`          | GET    | Existing       | —                                                  |
| 9 | `{baseurl}CalendarAbsentees/`   | GET    | Existing       | —                                                  |
|10 | `{baseurl}school_events/`       | GET    | Existing       | —                                                  |
|11 | `{baseurl}messages/`            | GET    | Existing       | —                                                  |
|12 | `{baseurl}videos/`              | GET    | Existing       | —                                                  |
|13 | `{baseurl}banners/`             | GET    | **NEW**        | `id`, `title`, `image`, `link_url`, `display_order` |
|14 | `{baseurl}exam_timetable/`      | GET    | Existing       | —                                                  |
|15 | `{baseurl}grievance/`           | GET    | Existing       | —                                                  |
|15 | `{baseurl}grievance/`           | POST   | Existing       | —                                                  |
|16 | `{baseurl}FcmSave/`             | POST   | Existing       | —                                                  |
|17 | `{baseurl}ResultDownload/`      | GET    | Existing       | Returns PDF binary                                 |
|18 | `{baseurl}timetable/`           | GET    | **NEW**        | `day`, `period_number`, `subject_name`, `subject_code`, `teacher_name` |

### Fields to add/verify in Django:

1. **`{homeurl}mobi/` response** — make sure the serializer includes:
   - `attendance_percentage` (float, nullable)
   - `homewk` (int, nullable — count of pending homework for this student)
   - `fee_status` (string, nullable — "Paid" / "Unpaid")
   - `school_student.logo` (string, nullable — relative media path)

2. **`{baseurl}school/` response** — make sure the serializer includes:
   - `website`
   - `web_gallery`
   - `web_contactus`
   - `web_aboutus`
   - `web_admission`

3. **`{baseurl}banners/`** — ✅ Done. Model, serializer, view, URL, admin, migration all added.

4. **`{baseurl}timetable/`** — ✅ Done. New endpoint returning the student's weekly class timetable.
   - `day` (string — `Mon`/`Tue`/`Wed`/`Thu`/`Fri`/`Sat`)
   - `period_number` (int)
   - `subject_name` (string)
   - `subject_code` (string)
   - `teacher_name` (string — first + last name)

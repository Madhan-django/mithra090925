# Mithran ERP — Mobile API Reference

**Base URL:** `https://mithran.co.in`  
**All endpoints require JWT Bearer token** (except the token endpoints).

---

## Authentication

### Obtain Token
```
POST /mobi/api/token/
Content-Type: application/json

{
  "username": "<student_username>",
  "password": "<student_password>"
}
```
**Response:**
```json
{
  "access": "<access_token>",
  "refresh": "<refresh_token>"
}
```

### Refresh Token
```
POST /mobi/api/token/refresh/
Content-Type: application/json

{
  "refresh": "<refresh_token>"
}
```
**Response:**
```json
{ "access": "<new_access_token>" }
```

**All subsequent requests must include:**
```
Authorization: Bearer <access_token>
```

---

## Student

### Get Student Profile + Attendance % + Homework Count + Fee Status
```
GET /mobi/?username=<username>
Authorization: Bearer <token>
```
**Response fields:** `id`, `first_name`, `last_name`, `roll_no`, `student_photo`, `class_name`, `secs`, `school_student`, `attendance_percentage`, `homewk` (int), `fee_status` (Paid / Unpaid / No Fees)

---

## Attendance

### Monthly Attendance Summary
```
GET /mobi/attendance/?username=<username>
Authorization: Bearer <token>
```
**Response:** Array of 12 months
```json
[
  { "month": "January", "attendance_data": 22, "absent": 1 },
  ...
]
```

### Calendar Absentees
```
GET /mobi/CalendarAbsentees/?username=<username>
Authorization: Bearer <token>
```
Returns full attendance records with dates and status (`Present` / `Absent`).

---

## Homework

### Homework (last 7 days)
```
GET /mobi/homework/?username=<username>
Authorization: Bearer <token>
```
**Response fields:** `id`, `title`, `description`, `homework_date`, `submission_date`, `hclass`, `secs`, `subj`, `created_by`

---

## Fees

### Individual Fee Details
```
GET /mobi/fee/?username=<username>
Authorization: Bearer <token>
```
Returns fee records for the student's current academic year.

---

## Notice Board

### Notices
```
GET /mobi/noticeboard/?username=<username>
Authorization: Bearer <token>
```

---

## Events

### School Events
```
GET /mobi/events/?username=<username>
Authorization: Bearer <token>
```
**Response fields:** `id`, `event_name`, `event_date`, `post_date`, `event_school`

---

## Exam Timetable

### Student Exam Schedule
```
GET /mobi/exam_timetable/?username=<username>
Authorization: Bearer <token>
```
**Response fields:** `exname` (exam info), `exam_subjects`, `paper_date`, `start_time`, `end_time`, `room_no`

---

## Results

### Download Result PDF
```
GET /mobi/ResultDownload/?username=<username>
Authorization: Bearer <token>
```
**Response:** `application/pdf` binary stream — save and open as PDF.

---

## Messages / Notifications

### Student Notifications
```
GET /mobi/messages/?username=<username>
Authorization: Bearer <token>
```

---

## Grievance

### List Grievances
```
GET /mobi/grievance/?username=<username>
Authorization: Bearer <token>
```

### Get Single Grievance
```
GET /mobi/grievance/<id>/?username=<username>
Authorization: Bearer <token>
```

### Submit Grievance
```
POST /mobi/grievance/?username=<username>
Authorization: Bearer <token>
Content-Type: application/json

{
  "area_of_complaint": "Academic",
  "detail": "Description of the issue",
  "mobile": "9876543210"
}
```
**Response:** Created grievance object with `id`, `complaint_status: "Open"`, `complaint_date`

---

## School Profile

### School Profile Info
```
GET /mobi/SchoolProfile/?username=<username>
Authorization: Bearer <token>
```
**Response fields:** `school_name`, `tagline`, `about`, `logo`, `founder_name`, `founder_pic`, `founded_year`, `city`, `phone`, `email`, `address`, `admission_open`, `admission_url`, `gallery_url`

---

## 🖼️ Mobile Banners

### Get Active Banners (slideshow)
```
GET /mobi/banners/?username=<username>
Authorization: Bearer <token>
```
**Response:**
```json
[
  {
    "id": 1,
    "title": "Annual Day 2025",
    "image": "https://mithran.co.in/media/school/banners/annual_day.jpg",
    "link_url": "https://example.com/event",
    "display_order": 0
  },
  {
    "id": 2,
    "title": "Admission Open",
    "image": "https://mithran.co.in/media/school/banners/admission.jpg",
    "link_url": "",
    "display_order": 1
  }
]
```
**Notes:**
- Only `is_active = true` banners are returned.
- Banners outside their `start_date` / `end_date` window are automatically excluded.
- Sorted by `display_order` ascending (0 = first slide).
- `image` is an absolute URL — load directly into `Glide` / `Picasso` / `Coil`.
- `link_url` may be empty string — only open browser if non-empty.

**Recommended Android implementation:**
```kotlin
// Retrofit call
interface MobiApi {
    @GET("mobi/banners/")
    suspend fun getBanners(
        @Query("username") username: String,
        @Header("Authorization") token: String
    ): List<BannerDto>
}

data class BannerDto(
    val id: Int,
    val title: String,
    val image: String,
    val link_url: String,
    val display_order: Int
)
```

---

## Video Gallery

### School Videos
```
GET /mobi/videos/?username=<username>
Authorization: Bearer <token>
```

---

## FCM Token (Push Notifications)

### Save / Update Device FCM Token
```
POST /mobi/FcmSave/?username=<username>
Authorization: Bearer <token>
Content-Type: application/json

{
  "firecmToken": "<firebase_device_token>"
}
```
Call this on every app launch after login to keep the token current.

---

## Staff Login

### Staff Authentication
```
GET /mobi/staff_login
Authorization: Bearer <token>
```
Returns staff profile for the authenticated user.

---

## Teacher Endpoints (Staff Token required)

### Get Classes
```
GET /mobi/teacher/classes/
Authorization: Bearer <staff_token>
```

### Get Sections for a Class
```
GET /mobi/teacher/sections/<class_id>/
Authorization: Bearer <staff_token>
```

### Get Subjects for a Class
```
GET /mobi/teacher/subjects/?class_id=<id>
Authorization: Bearer <staff_token>
```

### Get Students + Attendance for a Date
```
GET /mobi/teacher/students/<class_id>/<sec_id>/<YYYY-MM-DD>/
Authorization: Bearer <staff_token>
```

### Submit Attendance
```
POST /mobi/teacher/attendance/submit/
Authorization: Bearer <staff_token>
Content-Type: application/json

{
  "class_id": 1,
  "sec_id": 2,
  "date": "2025-08-14",
  "attendance": [
    { "student_id": 101, "status": "Present" },
    { "student_id": 102, "status": "Absent" }
  ]
}
```

### Get Teacher's Homework List
```
GET /mobi/teacher/homework/
Authorization: Bearer <staff_token>
```

### Add Homework
```
POST /mobi/teacher/homework/
Authorization: Bearer <staff_token>
Content-Type: application/json

{
  "class_id": 1,
  "sec_id": 2,
  "subject_id": 5,
  "title": "Chapter 3 Exercise",
  "description": "Complete all problems",
  "homework_date": "2025-08-14",
  "submission_date": "2025-08-16"
}
```

### Send Student Notification
```
POST /mobi/teacher/StudentNotification/
Authorization: Bearer <staff_token>
Content-Type: application/json

{
  "title": "Exam Alert",
  "message": "Unit test on Monday",
  "post_to": [101, 102, 103],
  "post_date": "2025-08-14T10:00:00",
  "status": "Active"
}
```

---

## Media Files

All `image`, `logo`, `student_photo` etc. fields return **relative paths**.  
Prepend the base URL to build the full URL:

```
https://mithran.co.in/media/<path_from_api>
```

Example:
```
https://mithran.co.in/media/school/banners/annual_day.jpg
```

> **Note:** The `/mobi/banners/` endpoint already returns **absolute URLs** for `image` — no prepending needed.

---

## HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200  | OK |
| 201  | Created |
| 400  | Bad request / missing params |
| 401  | Unauthorised — token missing or expired |
| 404  | Resource not found |
| 500  | Server error |

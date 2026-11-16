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

---

## Teacher leave (MithraTeach) — added 3 Nov 2026

Auth: `Authorization: Bearer <access token>` from `/mobi/api/token/` (same as other `/mobi/teacher/` APIs).

### GET `/mobi/teacher/leave/?year=2026`
```json
{
  "balance": {"total_cl": 12, "used_cl": 2, "pending_cl": 1, "remaining_cl": 10,
              "total_ml": 6, "used_ml": 0, "pending_ml": 0, "remaining_ml": 6, "lop": 1},
  "leave_types": [{"code": "CL", "name": "Casual Leave"}, {"code": "ML", "name": "Medical Leave"},
                  {"code": "LOP", "name": "Loss of Pay"}, {"code": "PERMISSION", "name": "Permission"}],
  "items": [{"id": 5, "leave_type": "CL", "leave_type_name": "Casual Leave", "from_date": "2026-11-06",
             "to_date": "2026-11-07", "days": 2.0, "from_time": null, "to_time": null, "reason": "...",
             "status": "Pending", "admin_remarks": "", "applied_on": "2026-11-03 10:15", "can_cancel": true}]
}
```

### POST `/mobi/teacher/leave/` (form-data or JSON)
Fields: `leave_type` (CL/ML/LOP/PERMISSION), `from_date` (YYYY-MM-DD), `to_date` (optional, = from_date if empty),
`from_time` + `to_time` (HH:MM, required for PERMISSION), `reason`, `attachment` (file, optional).
- 201 `{"success": true, "item": {...}}`
- 400 `{"success": false, "errors": ["Only 1 CL available ...", ...]}` — same checks as the web form
  (balance after pending, overlap, Sundays/holidays, finalized payroll, permission hours / per-month limit).

### POST `/mobi/teacher/leave/<id>/cancel/`
Cancels the teacher's own **Pending** request. Approved leave can only be cancelled by the office (web).

### Push notification
When the office approves / rejects / cancels a leave on the web, the teacher's device (staff.fcm_token, saved via
the existing FCM save API) gets a notification:
`title = "Leave approved"`, `data = {"type": "leave", "leave_id": "5", "status": "Approved"}` — open the leave screen on tap.

---

## Transport

### Get Bus Info + Live Location
```
GET /mobi/transport/?username=<username>
Authorization: Bearer <token>
```
Returns the student's bus assignment, stop timings, driver contact, and current GPS position.

**Response (student has transport allocation):**
```json
{
  "route": { "code": "R01", "name": "Coimbatore North Route" },
  "stop": {
    "name": "Gandhipuram",
    "area": "Town",
    "pickup_time": "07:30",
    "drop_time": "16:15"
  },
  "vehicle": { "name": "School Bus 4", "number": "TN33 AB 1234" },
  "driver":  { "name": "Rajan", "mobile": "9876543210" },
  "live": {
    "lat": 11.0168, "lng": 76.9558,
    "speed_kmh": 32.5, "heading": 180,
    "timestamp": "2026-11-16T07:42:00Z"
  }
}
```
`live` is `null` when the vehicle has no GPS position yet.  
`vehicle` and `driver` are `null` when no vehicle/driver is assigned to the route.

**Response (student not allocated to any route):**
```json
{ "transport": null }
```

### Boarding Push Notifications (automatic)
When staff marks boarding attendance, parents receive FCM notifications automatically:
- **Boarded:** "Ravi Kumar has boarded Coimbatore North Route at Gandhipuram (07:42 AM)."
- **Missed:** "Ravi Kumar has missed the morning bus at Gandhipuram. Please check."
- **Absent:** *(silent)*

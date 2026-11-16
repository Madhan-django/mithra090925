# Production Changes — Transport Parent APIs
**Date:** 2026-11-16  
**Branch:** main  
**No database migrations required.**

---

## Files Changed

### NEW: `transport/notify.py`
Helper that sends FCM push notifications to a student's registered devices when boarding attendance is marked.

### MODIFIED: `transport/views.py`
1. **Import** `send_boarding_fcm` from `transport.notify`.
2. **`gps_push` — security fix:** After looking up the vehicle, check for a `token` field (or `X-Api-Key` header) against `VTSVendor.api_key` for that school. If the school has VTSVendor records and the token doesn't match any of them, the push is rejected with HTTP 403. Schools with no VTSVendor records are unaffected (backward-compatible).
3. **`boarding_mark` — boarding alerts:** After each `BoardingAttendance` record is saved, calls `send_boarding_fcm()` for `Boarded` and `Missed` statuses. `Absent` is silent.

### MODIFIED: `mobi/views.py`
Added `TransportAPI` class at end of file — JWT-authenticated parent-facing endpoint.

### MODIFIED: `mobi/urls.py`
- Added `TransportAPI` to the import line.
- Added `path('transport/', TransportAPI.as_view(), name='transport_api')`.

---

## New API Endpoint

```
GET /mobi/transport/?username=<username>
Authorization: Bearer <access_token>
```

**Response (student has transport allocation):**
```json
{
  "route": {
    "code": "R01",
    "name": "Coimbatore North Route"
  },
  "stop": {
    "name": "Gandhipuram",
    "area": "Town",
    "pickup_time": "07:30",
    "drop_time": "16:15"
  },
  "vehicle": {
    "name": "School Bus 4",
    "number": "TN33 AB 1234"
  },
  "driver": {
    "name": "Rajan",
    "mobile": "9876543210"
  },
  "live": {
    "lat": 11.0168,
    "lng": 76.9558,
    "speed_kmh": 32.5,
    "heading": 180,
    "timestamp": "2026-11-16T07:42:00Z"
  }
}
```
`live` is `null` when the vehicle has no GPS position yet.

**Response (no transport allocation):**
```json
{ "transport": null }
```

---

## Boarding Notifications (automatic — no config needed)

When a staff member saves boarding attendance:

| Status  | Message sent to parent's app                                             |
|---------|--------------------------------------------------------------------------|
| Boarded | "Ravi Kumar has boarded Coimbatore North Route at Gandhipuram (07:42 AM)." |
| Missed  | "Ravi Kumar has missed the morning bus at Gandhipuram (Coimbatore North Route). Please check." |
| Absent  | *(silent — no notification)*                                             |

Notifications use the existing FCM infrastructure (`DeviceFCMToken` → `firebase_admin.messaging`). No new tables, no new config.

---

## GPS Push Security Fix

**Before:** Any HTTP client that knew a vehicle's `gps_device_id` could send fake locations.

**After:** If a school has one or more `VTSVendor` records, every push to `gps_push` must include a matching `api_key` value either as:
- JSON field: `"token": "<api_key>"`
- HTTP header: `X-Api-Key: <api_key>`

Schools with no `VTSVendor` records are unaffected — their existing GPS trackers keep working as before.

**To harden a school:** Go to Transport → VTS Vendors → Add Vendor. Set the `api_key` field to a strong random string. Give that string to the GPS tracker/vendor to include in each push.

---

## Deploy Steps

```bash
git pull origin main
# No migrations needed
python manage.py collectstatic --noinput
# Restart gunicorn / uwsgi
```

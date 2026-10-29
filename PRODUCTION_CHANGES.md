# Production Change Record
**Date:** 2026-09-25
**Scope:** Mobile API fixes — DJANGO_API_CHECKLIST.md alignment

---

## 1. Run Migrations

```bash
python manage.py migrate
```

Migrations to apply (if not already done on production):

| App | Migration file | What it adds |
|-----|----------------|--------------|
| `mobi` | `0002_schoolprofile.py` | SchoolProfile model |
| `mobi` | `0003_alter_schoolprofile_school_name.py` | SchoolProfile FK tweak |
| `mobi` | `0004_banner.py` | Banner model (new Home slideshow) |
| `institutions` | `0005_school_web_aboutus_school_web_admission_and_more.py` | `web_aboutus`, `web_contactus`, `web_gallery`, `web_admission` fields on school |
| `institutions` | `0006_school_group_code.py` through `0012_add_certificates_permission.py` | Various |

> Run `python manage.py showmigrations` first to confirm which are pending.

---

## 2. URL Changes (notify Android team / update any API docs)

| Old URL | New URL | Reason |
|---------|---------|--------|
| `mobi/events/` | `mobi/school_events/` | Renamed to match Android app expectation |
| _(missing)_ | `mobi/school/` | New — school info endpoint wired |

> **Android app:** If any internal link, deep-link, or cached URL references `mobi/events/`, update it to `mobi/school_events/`.

---

## 3. Code Changes (already applied to repo)

| File | Change |
|------|--------|
| `mobi/urls.py` | Renamed `events/` → `school_events/`; added `school/` path; imported `schoolapi` |
| `mobi/serializers.py` | Added `absent` field to `MonthlyAttendanceSerializer` |
| `mobi/serializers.py` | `SchoolProfileSerializer` — `school_name` now returns nested `{id, name}` instead of integer FK |
| `mobi/serializers.py` | `MessageSerializer` — restricted to `title`, `message`, `create_date` (was `__all__`) |
| `mobi/views.py` | `CalendarAbsenteesApi` — queryset now filters `status='Absent'` only |
| `mobi/views.py` | `SchoolProfileApi` — replaced `.get()` with `.filter().first()` + 404 guard |

---

## 4. Data Entry Required (manual — Django Admin)

- **Banner records:** Go to Django Admin → Mobi → Banners and add banners per school. The `mobi/banners/` endpoint returns nothing until records exist.
- **School Profile records:** Go to Django Admin → Mobi → School Profiles and ensure each school has a profile. `mobi/SchoolProfile/` returns 404 if no record exists for a school.
- **School web URLs:** Go to Django Admin → Institutions → Schools and fill in `web_aboutus`, `web_contactus`, `web_gallery`, `web_admission`, `website` for each school. These appear in `mobi/school/` response.

---

## 5. Restart Required

After deploying code changes:

```bash
# gunicorn / uwsgi — reload workers
sudo systemctl restart gunicorn   # or your process name
```

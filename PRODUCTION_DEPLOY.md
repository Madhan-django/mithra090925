# Production Deployment Checklist

Run these steps **in order** on the production server after pulling the latest code.

---

## 1. Pull Latest Code

```bash
git pull origin main
```

---

## 2. Install / Update Dependencies

```bash
pip install -r requirements.txt
```

---

## 3. Run Migrations

The following apps have new models that require migrations.

### 3a. `setup` app — `StaffAnnouncement` model

```bash
python manage.py makemigrations setup
python manage.py migrate setup
```

### 3b. `mobi` app — `GalleryPhoto` model (also includes `Banner` from previous session)

```bash
python manage.py makemigrations mobi
python manage.py migrate mobi
```

### 3c. `staff` app — `apps.py` schedule registration (no migration needed, just restart)

The 2 AM homework sync schedule is registered automatically via `post_migrate` signal.
Run any pending migration to trigger it, or manually run:

```bash
python manage.py migrate
```

This will register a Django-Q daily schedule `staff.tasks.sync_homework_all_schools` at 2:00 AM
in the `django_q_schedule` table. Verify it was created:

```sql
SELECT * FROM django_q_schedule WHERE func = 'staff.tasks.sync_homework_all_schools';
```

---

## 4. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

---

## 5. Verify Media Directories Exist

Ensure the following upload paths are writable under `MEDIA_ROOT`:

```
MEDIA_ROOT/school/banners/     ← Banner images
```

Create if missing:

```bash
mkdir -p /path/to/media/school/banners
```

---

## 6. Google Drive — Gallery Feature

The Photo Gallery uploads images to Google Drive using the service account already
configured for Lesson Plans (`GOOGLE_DRIVE_SERVICE_ACCOUNT_FILE` in settings).

No extra setup needed. Folder hierarchy on Drive will be:

```
<GOOGLE_DRIVE_ROOT_FOLDER_ID>/
  └── <SchoolName>/
        └── Gallery/
              └── <AlbumName>/
                    └── <photo files>
```

---

## 7. Restart Application Server

```bash
# Gunicorn / uWSGI — adjust to your setup
sudo systemctl restart gunicorn
# or
sudo supervisorctl restart mithran
```

---

## 8. Restart Django-Q Worker

The homework 2 AM sync task runs via the Django-Q cluster.

```bash
sudo supervisorctl restart django_q
# or
python manage.py qcluster   # foreground, for testing only
```

---

## 9. Post-Deploy Verification

| Check | How |
|---|---|
| Dashboard loads without error | Visit `/dashboard/` |
| Staff Announcements card visible | Dashboard right column, below What's New |
| Announcements CRUD works | `/setup/announcements/` |
| Photo Gallery list loads | `/mobi/gallery-manage/` |
| Photo upload works | Upload a test image, verify it appears on Drive |
| App API `/mobi/gallery/` responds | `GET /mobi/gallery/?username=<test_user>` |
| Homework sync schedule exists | Check Django-Q admin or SQL query above |

---

## 10. New Navigation Links (add to sidebar manually if needed)

These new panel URLs need to be added to your sidebar menu if your menu is DB-driven:

| Feature | URL Name | Path |
|---|---|---|
| Staff Announcements | `announcement_list` | `/setup/announcements/` |
| Photo Gallery | `gallery_list` | `/mobi/gallery-manage/` |

---

## Summary of Changes

| App | Change | Migration Required |
|---|---|---|
| `setup` | `StaffAnnouncement` model | YES |
| `mobi` | `GalleryPhoto` model | YES |
| `mobi` | `Banner` model (previous session) | YES (same migration run) |
| `staff` | `sync_homework_all_schools` task | NO |
| `staff` | `apps.py` 2 AM schedule registration | NO (runs on migrate) |
| `lessonplan` | `upload_gallery_photo()` drive util | NO |
| `dashboards` | Announcements card on home dashboard | NO |
| `mobiplayer` | Video gallery templates created | NO |

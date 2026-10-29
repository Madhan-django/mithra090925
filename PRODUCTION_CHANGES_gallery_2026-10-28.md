# PRODUCTION CHANGE GUIDE: Mobile Photo Gallery Fix
Date: 28-10-2026
Project: Nexora / Mithran ERP (Django) + Mithra Android app
Server change: ONE file only, `mobi/views.py`
Time needed: about 10 minutes
Downtime: only the restart in Step 6 (a few seconds)

---------------------------------------------------------------------

## 1. What was wrong

| # | Problem | Where | Effect |
|---|---------|-------|--------|
| 1 | The app expected JSON keys `p_title`, `p_link`, ... but Django sends `PTitle`, `Plink`, ... | Android: `model/PhotoItem.kt` | Gallery tiles were blank (no image, no title, tapping did nothing useful) |
| 2 | The admin "Gallery Manage" page saves photos to the `GalleryPhoto` model, but the app API `/mobi/photos/` only reads the `PhotoGallery` model | Django: `mobi/views.py` → `PhotoGalleryView` | Photos added from Gallery Manage never showed in the app |

This guide covers the **Django production change** (problem 2).
Problem 1 is fixed in the Android code. It reaches users when you publish a new APK (see Step 9).

## 2. What is NOT changing
- No model changes. **Do NOT run makemigrations or migrate.**
- No URL changes (`mobi/urls.py` is untouched).
- No new packages and no settings changes.
- No template changes.
- The API response format stays the same (a JSON list of photo objects with `P...` keys), so older app versions don't break.

---------------------------------------------------------------------

## STEP 1: Connect to the production server
1. RDP into the production Windows server.
2. Open the production project folder (the folder that contains `manage.py` and the `mobi` folder).

## STEP 2: Take a backup
1. Go to the `mobi` folder.
2. Copy `views.py` and rename the copy to:
   `views.py.bak_28102026`
3. Check that the backup file exists and is the same size as `views.py`.

## STEP 3: Check the imports (no change expected)
Open `mobi/views.py` in an editor (Notepad++ / VS Code / PyCharm).

**3a.** Near the top (around line 2), find:
```python
from .models import SchoolProfile, Banner, PhotoGallery, VideoGallery as VideoGalleryModel, GalleryPhoto
```
- If `GalleryPhoto` is already at the end, do nothing.
- If it is **missing**, add `, GalleryPhoto` at the end of that line.

**3b.** Find the `from .serializers import (` block (around lines 8-15). Make sure these names are in it:
- `schoolserializer`
- `PhotoGallerySerializer`

If either is missing, add it inside the brackets, separated by a comma.

**3c.** Make sure the `GalleryPhoto` model exists in production `mobi/models.py`:
search for `class GalleryPhoto(models.Model):`
- If it is **not there**, STOP. Production doesn't have the Gallery Manage feature yet, so this change isn't needed (and would crash). Deploy the Gallery Manage feature first.

## STEP 4: Find the code to replace
In `mobi/views.py`, search for:
```
class PhotoGalleryView(APIView):
```
The whole class currently looks like this (around lines 426-442):
```python
class PhotoGalleryView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.query_params.get('username')
        if not username:
            return Response({'error': 'username required'}, status=400)
        try:
            stud = students.objects.get(usernm=username)
        except students.DoesNotExist:
            return Response({'error': 'Student not found'}, status=404)
        sdata = school.objects.get(name=stud.school_student)
        photos = PhotoGallery.objects.filter(Pschool=sdata, status='active')
        serializer = PhotoGallerySerializer(photos, many=True)
        return Response(serializer.data)
```
**Only the LAST line changes**, along with the new lines that go before it. Everything above `return Response(serializer.data)` stays as it is.

## STEP 5: Make the change
Select this ONE line (the last line of `PhotoGalleryView.get`):
```python
        return Response(serializer.data)
```
⚠ Careful: `VideoGalleryView` (just below) also has `return Response(serializer.data)`. Change only the one inside **PhotoGalleryView**.

Replace it with these lines (8-space indent, same as the line you removed):
```python
        data = list(serializer.data)

        # Photos added from Gallery Manage (GalleryPhoto) — same shape as PhotoGallery
        school_data = schoolserializer(sdata).data
        for gp in GalleryPhoto.objects.filter(school=sdata, is_active=True):
            data.append({
                'id': f'g{gp.id}',
                'PTitle': gp.title,
                'PThumbnail': '',
                'Plink': gp.view_url,
                'Pdesc': gp.album,
                'Pdate': None,
                'Ppostdate': gp.created_at.date().isoformat() if gp.created_at else None,
                'Pschool': school_data,
                'status': 'active',
            })
        return Response(data)
```

### The final class should look EXACTLY like this:
```python
class PhotoGalleryView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.query_params.get('username')
        if not username:
            return Response({'error': 'username required'}, status=400)
        try:
            stud = students.objects.get(usernm=username)
        except students.DoesNotExist:
            return Response({'error': 'Student not found'}, status=404)
        sdata = school.objects.get(name=stud.school_student)
        photos = PhotoGallery.objects.filter(Pschool=sdata, status='active')
        serializer = PhotoGallerySerializer(photos, many=True)
        data = list(serializer.data)

        # Photos added from Gallery Manage (GalleryPhoto) — same shape as PhotoGallery
        school_data = schoolserializer(sdata).data
        for gp in GalleryPhoto.objects.filter(school=sdata, is_active=True):
            data.append({
                'id': f'g{gp.id}',
                'PTitle': gp.title,
                'PThumbnail': '',
                'Plink': gp.view_url,
                'Pdesc': gp.album,
                'Pdate': None,
                'Ppostdate': gp.created_at.date().isoformat() if gp.created_at else None,
                'Pschool': school_data,
                'status': 'active',
            })
        return Response(data)
```
Use **spaces, not tabs**. Save the file (keep UTF-8 encoding, because the comment contains a "—" character).

## STEP 6: Check for syntax errors BEFORE restarting
Open Command Prompt in the project folder (where `manage.py` is), activate the production virtualenv, then run:
```
python -m py_compile mobi\views.py
python manage.py check
```
- Both should finish with no errors (`check` says "System check identified no issues").
- If you get an error, fix it, or restore the backup (see ROLLBACK), before going on.

## STEP 7: Restart the application
Use whichever one your production setup uses:
- **IIS (wfastcgi):** IIS Manager → Application Pools → select the Nexora/Mithran pool → **Recycle**.
  (Or from an admin cmd: `%windir%\system32\inetsrv\appcmd recycle apppool /apppool.name:"<PoolName>"`)
- **Windows service / NSSM / waitress:** restart that service.
- **Linux gunicorn:** `sudo systemctl restart <service>`

No `collectstatic` or `migrate` is needed.

## STEP 8: Test in production
**8a. Test the API** (Postman):
1. Log in through the mobile login API to get a JWT token (the same way the app does).
2. Send `GET https://mithran.co.in/mobi/photos/?username=<student_username>`
   with header `Authorization: Bearer <token>`.
3. Expected result: status **200**, and a JSON list where each item has `PTitle`, `Plink`, `Pschool` and so on.
   - Old `PhotoGallery` items have number ids (e.g. `"id": 5`).
   - Gallery Manage items have ids that start with `g` (e.g. `"id": "g3"`).

**8b. Test end to end:**
1. Log in to the web ERP as Admin → Gallery Manage → Add a test photo (upload or Drive link) and tick Active.
2. Call the API again (8a). The new photo should appear.
3. In the app (a NEW build, see Step 9), open Photo Gallery and pull to refresh. The photo should show with its title, and open when tapped.
4. Delete the test photo from Gallery Manage if you don't need it.

**8c. Check the logs:** look at the IIS / Django error log for any new errors on `/mobi/photos/`.

## STEP 9: Android app (needed for users to SEE the photos)
The production server change alone won't fix the blank tiles in the CURRENTLY installed app. Problem 1 is in the app.

File: `app/src/main/java/com/nexis/mithra/model/PhotoItem.kt` (already changed locally)
```kotlin
package com.nexis.mithra.model

import com.google.gson.annotations.SerializedName

data class PhotoItem(
    val id: String?,
    @SerializedName("PTitle")     val PTitle: String?,
    @SerializedName("PThumbnail") val PThumbnail: String?,
    @SerializedName("Plink")      val Plink: String?,
    @SerializedName("Pdesc")      val Pdesc: String?,
    @SerializedName("Pdate")      val Pdate: String?,
    @SerializedName("Ppostdate")  val Ppostdate: String?,
    @SerializedName("Pschool")    val Pschool: Vschool?,
    val status: String?
)
```
Before you build the release:
1. In `Auth.kt`, switch the URLs back to production. Comment out the `10.0.2.2:8000` lines and uncomment the `https://mithran.co.in/...` lines.
2. Increase `versionCode` / `versionName` in `app/build.gradle.kts`.
3. Build → Generate Signed Bundle/APK → upload to Play Store / share the APK.

Order: deploy Django first (Steps 1-8), then release the app. The new app works with both the old and the new server code.

---------------------------------------------------------------------

## ROLLBACK (if anything goes wrong)
1. In the `mobi` folder, delete or rename the edited `views.py`.
2. Rename `views.py.bak_28102026` back to `views.py`.
3. Recycle the app pool / restart the service (Step 7).
4. Run the API test (8a) again to confirm it's back to the old behaviour.

No database changes were made, so no DB rollback is needed.

---------------------------------------------------------------------

## CHECKLIST
- [ ] Step 2: backup `views.py.bak_28102026` created
- [ ] Step 3: imports checked (`GalleryPhoto`, `schoolserializer`, `PhotoGallerySerializer`)
- [ ] Step 3c: `GalleryPhoto` model exists in production
- [ ] Step 5: only `PhotoGalleryView` changed (not `VideoGalleryView`)
- [ ] Step 6: `py_compile` and `manage.py check` passed
- [ ] Step 7: app pool recycled / service restarted
- [ ] Step 8: API returns 200 with Gallery Manage photos included
- [ ] Step 9: new APK built with production URLs and a higher versionCode

---------------------------------------------------------------------

## Reference: exact diff (local dev copy)
```diff
--- mobi/views.py (before)
+++ mobi/views.py (after)
@@ -438,7 +438,23 @@
         sdata = school.objects.get(name=stud.school_student)
         photos = PhotoGallery.objects.filter(Pschool=sdata, status='active')
         serializer = PhotoGallerySerializer(photos, many=True)
-        return Response(serializer.data)
+        data = list(serializer.data)
+
+        # Photos added from Gallery Manage (GalleryPhoto) — same shape as PhotoGallery
+        school_data = schoolserializer(sdata).data
+        for gp in GalleryPhoto.objects.filter(school=sdata, is_active=True):
+            data.append({
+                'id': f'g{gp.id}',
+                'PTitle': gp.title,
+                'PThumbnail': '',
+                'Plink': gp.view_url,
+                'Pdesc': gp.album,
+                'Pdate': None,
+                'Ppostdate': gp.created_at.date().isoformat() if gp.created_at else None,
+                'Pschool': school_data,
+                'status': 'active',
+            })
+        return Response(data)
 
 
 class VideoGalleryView(APIView):
```

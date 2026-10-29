# PRODUCTION DEPLOYMENT: Django changes (Mobile Gallery / Album Slideshow)
Date prepared: 28-10-2026
Project: Nexora / Mithran ERP (Django), production at mithran.co.in

**This ONE file has every Django change from 28-10-2026.** Follow it from top to bottom.
(It replaces the separate Part 1 and Part 2 guides. Video changes are Android-only, so there's no Django change for videos.)

---------------------------------------------------------------------

## SUMMARY

### What the changes do
1. **Gallery Manage photos now reach the app.** `/mobi/photos/` returns both `PhotoGallery` records AND `GalleryPhoto` records (photos added from the web page "Gallery Manage").
2. **Album slideshow.** A gallery entry's link can be an album, and the app shows all its photos as a slideshow:
   | Link | Result |
   |---|---|
   | Website album page, e.g. `https://jacobindia.edu.in/album.php?slug=independence-day-2026-jnps` | All photos on that page |
   | Web folder (directory listing) | All images in the folder |
   | Google Drive folder `drive.google.com/drive/folders/...` | All images in the folder |
   | Google Drive file / direct image URL (.jpg/.png...) | That single image |
   | A page with no readable photos | The app opens it in the browser |
3. **Automatic cover image.** If an entry has no thumbnail, the first photo of its album is used.
4. **New API:** `GET /mobi/photos/album/?username=<student>&id=<id from /mobi/photos/>`

### Files
| # | File | Type of change |
|---|------|----------------|
| 1 | `mobi/web_album.py` | **NEW FILE**, copy as is |
| 2 | `lessonplan/drive_utils.py` | add 1 function `list_folder_images()` |
| 3 | `mobi/views.py` | 3 imports + replace class `PhotoGalleryView` + add a new block (helpers + `PhotoAlbumView`) |
| 4 | `mobi/urls.py` | 1 import name + 1 URL |

### NOT needed
- No `makemigrations` / `migrate` (no model changes)
- No `pip install` (only the Python standard library and the existing Google Drive client)
- No `collectstatic`, no settings changes, no template changes

### Time: about 20 minutes. Downtime: only the app pool recycle.

---------------------------------------------------------------------

## STEP 0: Before you start
1. RDP into the production server and open the project folder (the one with `manage.py`).
2. Check these exist in production (they come from the earlier Gallery Manage / LMS work):
   - `mobi/models.py` has `class GalleryPhoto(models.Model):` and `class PhotoGallery(models.Model):`
   - `lessonplan/drive_utils.py` has `def _get_service():` and `def delete_note(file_id):`
   - `settings.py` has `GOOGLE_DRIVE_SERVICE_ACCOUNT_FILE`, and that json file is on the server
   - **If any of these is missing, STOP.** Deploy the Gallery Manage / Drive feature first.
3. Check the server can open outside websites (needed for website album links):
   open `https://jacobindia.edu.in` in a browser ON the server.

## STEP 1: Backup
Make a folder `_backup_<today's date>` in the project and copy these into it:
- `mobi\views.py`
- `mobi\urls.py`
- `lessonplan\drive_utils.py`

---------------------------------------------------------------------

## STEP 2: NEW FILE `mobi/web_album.py`
Copy `mobi\web_album.py` from the dev project (`C:\Users\Madhan\PycharmProjects\mithra200826\mobi\web_album.py`)
into the production `mobi` folder, next to `views.py`.

Or create the file and paste the full contents below:
```python
"""
Read photos from a website album page or a web folder (directory listing).
e.g. https://jacobindia.edu.in/album.php?slug=independence-day-2026-jnps

Uses only the Python standard library (no extra pip packages).

How images are picked:
  1. Links to image files  <a href="photo1.jpg">  (lightbox galleries, web folders)
     → if any exist, ONLY these are used (they are the full-size album photos)
  2. Otherwise all <img> / <source> images on the page
     (data-src / data-original / srcset supported for lazy-loaded galleries)
  Images inside <header>, <nav>, <footer>, and logos / icons / tiny images, are skipped.
"""
import ipaddress
import re
import socket
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse
from urllib.request import Request, build_opener, HTTPRedirectHandler

IMAGE_EXT_RE = re.compile(r'\.(?:jpe?g|png|gif|webp|bmp)(?:[?#].*)?$', re.IGNORECASE)
SKIP_RE = re.compile(
    r'(logo|icon|favicon|sprite|avatar|loader|loading|spinner|placeholder|blank\.|pixel|'
    r'facebook|twitter|instagram|youtube|whatsapp|linkedin|arrow|btn[_-]|button)',
    re.IGNORECASE,
)
SKIP_SECTIONS = ('header', 'nav', 'footer')
MAX_BYTES = 5 * 1024 * 1024
TIMEOUT = 10
USER_AGENT = ('Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 '
              '(KHTML, like Gecko) Chrome/120.0 Mobile Safari/537.36')


def _is_public_host(url):
    """Block localhost / private network addresses (safety)."""
    try:
        parsed = urlparse(url)
        if parsed.scheme not in ('http', 'https') or not parsed.hostname:
            return False
        for info in socket.getaddrinfo(parsed.hostname, None):
            ip = ipaddress.ip_address(info[4][0])
            if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved or ip.is_multicast:
                return False
        return True
    except Exception:
        return False


class _SafeRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not _is_public_host(newurl):
            return None
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def _best_from_srcset(srcset):
    """Pick the largest candidate from a srcset string."""
    best, best_w = None, -1
    for part in (srcset or '').split(','):
        bits = part.strip().split()
        if not bits:
            continue
        w = 0
        if len(bits) > 1:
            m = re.match(r'(\d+(?:\.\d+)?)[wx]', bits[1])
            if m:
                w = float(m.group(1))
        if w > best_w:
            best, best_w = bits[0], w
    return best


def _small(value):
    try:
        return int(re.sub(r'[^\d]', '', value or '') or 999) < 80
    except ValueError:
        return False


class _AlbumParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.link_images = []
        self.img_images = []
        self.skip_depth = 0

    def handle_starttag(self, tag, attrs):
        a = {k: (v or '') for k, v in attrs}
        if tag in SKIP_SECTIONS:
            self.skip_depth += 1
            return
        if self.skip_depth:
            return

        if tag == 'a':
            for key in ('href', 'data-src', 'data-href', 'data-image', 'data-full', 'data-large'):
                val = a.get(key, '').strip()
                if val and IMAGE_EXT_RE.search(val):
                    self.link_images.append(val)
                    break

        elif tag in ('img', 'source'):
            if _small(a.get('width')) or _small(a.get('height')):
                return
            if SKIP_RE.search(a.get('class', '') + ' ' + a.get('alt', '') + ' ' + a.get('id', '')):
                return
            src = None
            for key in ('data-full', 'data-large', 'data-original', 'data-lazy-src', 'data-src'):
                if a.get(key, '').strip():
                    src = a[key].strip()
                    break
            if not src:
                src = _best_from_srcset(a.get('data-srcset') or a.get('srcset'))
            if not src:
                src = a.get('src', '').strip()
            if src and not src.startswith('data:'):
                self.img_images.append(src)

    def handle_endtag(self, tag):
        if tag in SKIP_SECTIONS and self.skip_depth:
            self.skip_depth -= 1


def fetch_album_images(url):
    """
    Return a list of absolute image URLs found on the web page / folder at `url`.
    Returns [] on any error or when nothing is found.
    """
    url = (url or '').strip()
    if not _is_public_host(url):
        return []
    try:
        opener = build_opener(_SafeRedirect)
        req = Request(url, headers={'User-Agent': USER_AGENT, 'Accept': 'text/html,image/*,*/*'})
        with opener.open(req, timeout=TIMEOUT) as resp:
            final_url = resp.geturl()
            ctype = resp.headers.get('Content-Type', '')
            if ctype.startswith('image/'):
                return [final_url]
            charset = resp.headers.get_content_charset() or 'utf-8'
            html = resp.read(MAX_BYTES).decode(charset, errors='replace')
    except Exception as e:
        print(f'Web album fetch error for {url}: {e}')
        return []

    parser = _AlbumParser()
    try:
        parser.feed(html)
    except Exception as e:
        print(f'Web album parse error for {url}: {e}')

    from_links = bool(parser.link_images)
    candidates = parser.link_images if from_links else parser.img_images

    result, seen = [], set()
    for c in candidates:
        full = urljoin(final_url, c.replace('&amp;', '&'))
        if not full.startswith(('http://', 'https://')):
            continue
        path = urlparse(full).path.lower()
        if path.endswith('.svg') or SKIP_RE.search(path.rsplit('/', 1)[-1]):
            continue
        if not from_links and not IMAGE_EXT_RE.search(full) and '.' in path.rsplit('/', 1)[-1]:
            # <img> pointing to a non-image file type (e.g. .svg, .ico) → skip
            continue
        if full in seen:
            continue
        seen.add(full)
        result.append(full)
    return result
```

---------------------------------------------------------------------

## STEP 3: `lessonplan/drive_utils.py`: add one function
Open the file and find:
```python
def delete_note(file_id):
```
Just ABOVE that line, paste the following (leave 2 blank lines after it, before `def delete_note`):
```python
def list_folder_images(folder_id):
    """
    List all image files directly inside a Drive folder (sorted by name).
    The folder must be shared 'Anyone with the link' or shared with the service account.
    Returns [{'id': ..., 'name': ...}, ...].
    """
    service = _get_service()
    images = []
    page_token = None
    while True:
        res = service.files().list(
            q=f"'{folder_id}' in parents and mimeType contains 'image/' and trashed=false",
            fields='nextPageToken, files(id, name)',
            orderBy='name',
            pageSize=1000,
            pageToken=page_token,
            supportsAllDrives=True,
            includeItemsFromAllDrives=True,
        ).execute()
        images.extend(res.get('files', []))
        page_token = res.get('nextPageToken')
        if not page_token:
            break
    return images
```

---------------------------------------------------------------------

## STEP 4: `mobi/views.py`: imports
**4a.** Near the top, find:
```python
import calendar
import os
```
Change to:
```python
import calendar
import os
import re
import hashlib
from django.core.cache import cache
```
(Don't add a line twice if it's already there. Make sure nothing else in views.py is named `cache`.)

**4b.** Line 2 must import `GalleryPhoto` (add it at the end if it's missing):
```python
from .models import SchoolProfile, Banner, PhotoGallery, VideoGallery as VideoGalleryModel, GalleryPhoto
```
**4c.** The `from .serializers import (...)` block must include `schoolserializer` and `PhotoGallerySerializer` (add them if missing).

---------------------------------------------------------------------

## STEP 5: `mobi/views.py`: replace the whole class `PhotoGalleryView`
Search for `class PhotoGalleryView(APIView):`.
Select from that line down to the line just BEFORE `class VideoGalleryView(APIView):`.

**The production code you're replacing (original) looks like this:**
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

**Replace it with the following (Step 5 code + Step 6 block, in this order):**

### 5a. New PhotoGalleryView
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

        # No thumbnail (Drive folder / website album / image link) → first image as cover
        for item in data:
            if not item.get('PThumbnail'):
                try:
                    imgs = _album_images(item.get('Plink') or '')
                    if imgs:
                        item['PThumbnail'] = imgs[0]['thumb']
                except Exception as e:
                    print(f"Gallery cover error for {item.get('Plink')}: {e}")
        return Response(data)
```

## STEP 6: `mobi/views.py`: add the new block right after PhotoGalleryView
Directly after the new `PhotoGalleryView` (Step 5a), and BEFORE `class VideoGalleryView(APIView):`, paste:
```python
# ── Photo album slideshow (Drive folder / website album page) ─────────────

DRIVE_FOLDER_RE = re.compile(r'drive\.google\.com/drive/(?:u/\d+/)?folders/([a-zA-Z0-9_-]+)')
DRIVE_FILE_RE = re.compile(r'drive\.google\.com/(?:file/d/|open\?id=|uc\?(?:export=\w+&)?id=)([a-zA-Z0-9_-]+)')
IMAGE_URL_RE = re.compile(r'\.(?:jpe?g|png|gif|webp|bmp)(?:\?.*)?$', re.IGNORECASE)


def _drive_folder_id(link):
    m = DRIVE_FOLDER_RE.search(link or '')
    return m.group(1) if m else None


def _drive_file_id(link):
    m = DRIVE_FILE_RE.search(link or '')
    return m.group(1) if m else None


def _is_image_url(link):
    return bool(IMAGE_URL_RE.search((link or '').strip()))


def _drive_thumb(file_id, size):
    return f'https://drive.google.com/thumbnail?id={file_id}&sz=w{size}'


def _album_img(img_id, name, thumb, full):
    return {'id': img_id, 'name': name, 'thumb': thumb, 'full': full}


def _album_images(link):
    """
    All photos for a gallery link (cached 10 minutes):
      Drive folder            → every image in the folder
      Drive file / image URL  → that one image
      Website album page /
      web folder listing      → every album image on that page
    Returns [] when nothing is found. Raises only on Drive API errors.
    """
    link = (link or '').strip()
    if not link:
        return []
    key = 'gallery_album_' + hashlib.md5(link.encode('utf-8')).hexdigest()
    images = cache.get(key)
    if images is not None:
        return images

    folder_id = _drive_folder_id(link)
    file_id = _drive_file_id(link)
    if folder_id:
        from lessonplan.drive_utils import list_folder_images
        images = [
            _album_img(f['id'], f.get('name', ''), _drive_thumb(f['id'], 400), _drive_thumb(f['id'], 2048))
            for f in list_folder_images(folder_id)
        ]
    elif file_id:
        images = [_album_img(file_id, '', _drive_thumb(file_id, 400), _drive_thumb(file_id, 2048))]
    elif _is_image_url(link) or not link.startswith('http'):
        images = [_album_img(link, '', link, link)]
    else:
        from .web_album import fetch_album_images
        images = [
            _album_img(u, u.rsplit('/', 1)[-1].split('?')[0], u, u)
            for u in fetch_album_images(link)
        ]

    # empty result cached only 2 minutes so a temporarily-down website is retried soon
    cache.set(key, images, 600 if images else 120)
    return images


class PhotoAlbumView(APIView):
    """
    GET /mobi/photos/album/?username=<usernm>&id=<photo id from /mobi/photos/>
    Returns {"title": ..., "images": [{"id","name","thumb","full"}, ...]}
    If no images can be found: {"title": ..., "images": [], "web_url": <link>} → app opens browser
    id = number  → PhotoGallery
    id = g<num>  → GalleryPhoto (Gallery Manage)
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.query_params.get('username')
        photo_id = request.query_params.get('id', '')
        if not username or not photo_id:
            return Response({'error': 'username and id required'}, status=400)
        try:
            stud = students.objects.get(usernm=username)
        except students.DoesNotExist:
            return Response({'error': 'Student not found'}, status=404)
        sdata = school.objects.get(name=stud.school_student)

        title, link = '', ''
        if photo_id.startswith('g') and photo_id[1:].isdigit():
            gp = GalleryPhoto.objects.filter(pk=int(photo_id[1:]), school=sdata, is_active=True).first()
            if gp:
                title, link = gp.title, gp.view_url
        elif photo_id.isdigit():
            pg = PhotoGallery.objects.filter(pk=int(photo_id), Pschool=sdata, status='active').first()
            if pg:
                title, link = pg.PTitle, pg.Plink
        if not link:
            return Response({'error': 'Album not found'}, status=404)

        try:
            images = _album_images(link)
        except Exception as e:
            return Response({'error': f'Could not read album: {e}'}, status=502)

        if images:
            return Response({'title': title, 'images': images})
        return Response({'title': title, 'images': [], 'web_url': link})
```
Keep 2 blank lines between the classes/blocks.

⚠ Don't touch `class VideoGalleryView`. It also ends with `return Response(serializer.data)`, but it stays as it is.

After Steps 5 and 6, the order in `views.py` is:
```
class PhotoGalleryView(APIView):        ← replaced (5a)
# ── Photo album slideshow ...           ← new block (6)
DRIVE_FOLDER_RE / DRIVE_FILE_RE / IMAGE_URL_RE
def _drive_folder_id / _drive_file_id / _is_image_url / _drive_thumb / _album_img / _album_images
class PhotoAlbumView(APIView):
class VideoGalleryView(APIView):        ← unchanged
```

---------------------------------------------------------------------

## STEP 7: `mobi/urls.py`
**7a.** In the `from .views import (...)` block, find:
```python
                    PhotoGalleryView,
```
Change to:
```python
                    PhotoGalleryView, PhotoAlbumView,
```
**7b.** In `urlpatterns`, find:
```python
    path('photos/', PhotoGalleryView.as_view(), name='photos'),
```
Add this line directly BELOW it:
```python
    path('photos/album/', PhotoAlbumView.as_view(), name='photo_album'),
```

---------------------------------------------------------------------

## STEP 8: Check for errors (BEFORE restarting)
Open Command Prompt in the project folder and activate the production venv:
```
python -m py_compile mobi\web_album.py
python -m py_compile lessonplan\drive_utils.py
python -m py_compile mobi\views.py
python -m py_compile mobi\urls.py
python manage.py check
```
All should pass ("System check identified no issues").
If anything fails, fix it, or restore the backups (ROLLBACK), before going on.

Quick check that the server can read a website album:
```
python -c "import sys; sys.path.insert(0,'mobi'); import web_album; r=web_album.fetch_album_images('https://jacobindia.edu.in/album.php?slug=independence-day-2026-jnps'); print(len(r)); print(r[:3])"
```
It should print the number of photos found and the first 3 photo URLs.
`0` means: the page needs a login, the photos are loaded by JavaScript, or outbound internet is blocked.

## STEP 9: Restart
IIS Manager → Application Pools → the Nexora/Mithran pool → **Recycle**
(or from an admin cmd: `%windir%\system32\inetsrv\appcmd recycle apppool /apppool.name:"<PoolName>"`)

---------------------------------------------------------------------

## STEP 10: Test in production (Postman)
Get a JWT token from the mobile login API (the same way the app does). Then use the header `Authorization: Bearer <token>` on these calls:

1. `GET https://mithran.co.in/mobi/photos/?username=<student>`
   - 200, a JSON list. Items from Gallery Manage have ids like `"g12"`, older items have number ids.
   - Album entries with no thumbnail now have `PThumbnail` filled in.
2. In the web ERP → Gallery Manage → Add → **link** option → paste a website album link → Active → Save.
   Call (1) again; the new entry should appear.
3. `GET https://mithran.co.in/mobi/photos/album/?username=<student>&id=g12`
   - `{"title": ..., "images": [{"id","name","thumb","full"}, ...]}` with all the photos
   - `"images": [], "web_url": ...` → no photos could be read (see the quick check in Step 8)
   - `502 Could not read album` → a Drive folder that isn't shared ("Anyone with the link → Viewer")
4. Check the IIS / Django error log for new errors on `/mobi/photos/`.

Note: album photo lists are cached for 10 minutes (2 minutes if empty). An app pool recycle clears the cache.

### Drive folders used as albums
Share each one: Drive → right-click the folder → Share → General access → **Anyone with the link → Viewer**.
(Service account, if you need it: `mithran-lms-storage@mithran-erp-drive.iam.gserviceaccount.com`)

---------------------------------------------------------------------

## ROLLBACK
1. Copy the 3 backed-up files back (`views.py`, `urls.py`, `drive_utils.py`).
2. Delete (or rename) `mobi\web_album.py`.
3. Recycle the app pool.
No database changes were made, so there's nothing to undo in the DB.

---------------------------------------------------------------------

## AFTER THE SERVER: Android app release
The server changes work with the CURRENT app (no crash). The new gallery features need the new APK:
- Photo gallery JSON fix, album slideshow, in-app video player (Media3), video gallery JSON fix.
- Before building: `Auth.kt` → production URLs (`https://mithran.co.in/...`), bump `versionCode` / `versionName` (currently 28 / "28.0"), Gradle sync, then a signed build.
- Order: **server first, then the app.**
- Still to test before release: login/logout and an older phone (Android 7.0 emulator "Small Phone"), planned for tomorrow.

---------------------------------------------------------------------

## CHECKLIST
- [ ] Step 0 prerequisites present (GalleryPhoto, PhotoGallery, drive_utils, service account json, outbound internet)
- [ ] Step 1 backups taken
- [ ] Step 2 `mobi/web_album.py` added
- [ ] Step 3 `list_folder_images()` added to drive_utils.py
- [ ] Step 4 imports (`re`, `hashlib`, `cache`, `GalleryPhoto`, `schoolserializer`, `PhotoGallerySerializer`)
- [ ] Step 5 PhotoGalleryView replaced
- [ ] Step 6 new block added above VideoGalleryView (VideoGalleryView not changed)
- [ ] Step 7 urls.py import + path
- [ ] Step 8 py_compile + `manage.py check` + web album quick check passed
- [ ] Step 9 app pool recycled
- [ ] Step 10 Postman tests pass
- [ ] Drive album folders shared "Anyone with the link"

---------------------------------------------------------------------

## REFERENCE: full diffs (original → new), from the dev copy
```diff
--- mobi/views.py (original)
+++ mobi/views.py (new)
@@ -40,6 +40,9 @@
 from django.utils import timezone
 import calendar
 import os
+import re
+import hashlib
+from django.core.cache import cache
 
 # Create your views here.
 
@@ -438,7 +441,147 @@
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
+
+        # No thumbnail (Drive folder / website album / image link) → first image as cover
+        for item in data:
+            if not item.get('PThumbnail'):
+                try:
+                    imgs = _album_images(item.get('Plink') or '')
+                    if imgs:
+                        item['PThumbnail'] = imgs[0]['thumb']
+                except Exception as e:
+                    print(f"Gallery cover error for {item.get('Plink')}: {e}")
+        return Response(data)
+
+
+# ── Photo album slideshow (Drive folder / website album page) ─────────────
+
+DRIVE_FOLDER_RE = re.compile(r'drive\.google\.com/drive/(?:u/\d+/)?folders/([a-zA-Z0-9_-]+)')
+DRIVE_FILE_RE = re.compile(r'drive\.google\.com/(?:file/d/|open\?id=|uc\?(?:export=\w+&)?id=)([a-zA-Z0-9_-]+)')
+IMAGE_URL_RE = re.compile(r'\.(?:jpe?g|png|gif|webp|bmp)(?:\?.*)?$', re.IGNORECASE)
+
+
+def _drive_folder_id(link):
+    m = DRIVE_FOLDER_RE.search(link or '')
+    return m.group(1) if m else None
+
+
+def _drive_file_id(link):
+    m = DRIVE_FILE_RE.search(link or '')
+    return m.group(1) if m else None
+
+
+def _is_image_url(link):
+    return bool(IMAGE_URL_RE.search((link or '').strip()))
+
+
+def _drive_thumb(file_id, size):
+    return f'https://drive.google.com/thumbnail?id={file_id}&sz=w{size}'
+
+
+def _album_img(img_id, name, thumb, full):
+    return {'id': img_id, 'name': name, 'thumb': thumb, 'full': full}
+
+
+def _album_images(link):
+    """
+    All photos for a gallery link (cached 10 minutes):
+      Drive folder            → every image in the folder
+      Drive file / image URL  → that one image
+      Website album page /
+      web folder listing      → every album image on that page
+    Returns [] when nothing is found. Raises only on Drive API errors.
+    """
+    link = (link or '').strip()
+    if not link:
+        return []
+    key = 'gallery_album_' + hashlib.md5(link.encode('utf-8')).hexdigest()
+    images = cache.get(key)
+    if images is not None:
+        return images
+
+    folder_id = _drive_folder_id(link)
+    file_id = _drive_file_id(link)
+    if folder_id:
+        from lessonplan.drive_utils import list_folder_images
+        images = [
+            _album_img(f['id'], f.get('name', ''), _drive_thumb(f['id'], 400), _drive_thumb(f['id'], 2048))
+            for f in list_folder_images(folder_id)
+        ]
+    elif file_id:
+        images = [_album_img(file_id, '', _drive_thumb(file_id, 400), _drive_thumb(file_id, 2048))]
+    elif _is_image_url(link) or not link.startswith('http'):
+        images = [_album_img(link, '', link, link)]
+    else:
+        from .web_album import fetch_album_images
+        images = [
+            _album_img(u, u.rsplit('/', 1)[-1].split('?')[0], u, u)
+            for u in fetch_album_images(link)
+        ]
+
+    # empty result cached only 2 minutes so a temporarily-down website is retried soon
+    cache.set(key, images, 600 if images else 120)
+    return images
+
+
+class PhotoAlbumView(APIView):
+    """
+    GET /mobi/photos/album/?username=<usernm>&id=<photo id from /mobi/photos/>
+    Returns {"title": ..., "images": [{"id","name","thumb","full"}, ...]}
+    If no images can be found: {"title": ..., "images": [], "web_url": <link>} → app opens browser
+    id = number  → PhotoGallery
+    id = g<num>  → GalleryPhoto (Gallery Manage)
+    """
+    authentication_classes = [JWTAuthentication]
+    permission_classes = [IsAuthenticated]
+
+    def get(self, request):
+        username = request.query_params.get('username')
+        photo_id = request.query_params.get('id', '')
+        if not username or not photo_id:
+            return Response({'error': 'username and id required'}, status=400)
+        try:
+            stud = students.objects.get(usernm=username)
+        except students.DoesNotExist:
+            return Response({'error': 'Student not found'}, status=404)
+        sdata = school.objects.get(name=stud.school_student)
+
+        title, link = '', ''
+        if photo_id.startswith('g') and photo_id[1:].isdigit():
+            gp = GalleryPhoto.objects.filter(pk=int(photo_id[1:]), school=sdata, is_active=True).first()
+            if gp:
+                title, link = gp.title, gp.view_url
+        elif photo_id.isdigit():
+            pg = PhotoGallery.objects.filter(pk=int(photo_id), Pschool=sdata, status='active').first()
+            if pg:
+                title, link = pg.PTitle, pg.Plink
+        if not link:
+            return Response({'error': 'Album not found'}, status=404)
+
+        try:
+            images = _album_images(link)
+        except Exception as e:
+            return Response({'error': f'Could not read album: {e}'}, status=502)
+
+        if images:
+            return Response({'title': title, 'images': images})
+        return Response({'title': title, 'images': [], 'web_url': link})
 
 
 class VideoGalleryView(APIView):
```

```diff
--- mobi/urls.py (original)
+++ mobi/urls.py (new)
@@ -6,7 +6,7 @@
                     ClassesAPI, SectionsAPI, StudentsAttendanceAPI, SubmitAttendanceAPI, SubjectsAPI, TeacherHomeworkAddAPI, GeneralNotificationAPI,
                     GrievanceAPI,
                     BannerAPI, banner_list, banner_add, banner_edit, banner_delete,
-                    PhotoGalleryView,
+                    PhotoGalleryView, PhotoAlbumView,
                     gallery_list, gallery_add, gallery_delete)
 from rest_framework_simplejwt.views import (
     TokenObtainPairView,
@@ -29,6 +29,7 @@
     path('CalendarAbsentees/', CalendarAbsenteesApi.as_view(), name='CalendarAbsentees'),
     path('ResultDownload/', ResultDownload.as_view(), name='ResultDownload'),
     path('photos/', PhotoGalleryView.as_view(), name='photos'),
+    path('photos/album/', PhotoAlbumView.as_view(), name='photo_album'),
     path('videos/', VideoGalleryView.as_view(), name='videos'),
     path('SchoolProfile/', SchoolProfileApi.as_view(), name='SchoolProfile'),
     path('school-profile/', schprofile_list, name='schprofile_list'),
```

```diff
--- lessonplan/drive_utils.py (original)
+++ lessonplan/drive_utils.py (new)
@@ -148,6 +148,32 @@
     return file_id, info.get('webViewLink', '')
 
 
+def list_folder_images(folder_id):
+    """
+    List all image files directly inside a Drive folder (sorted by name).
+    The folder must be shared 'Anyone with the link' or shared with the service account.
+    Returns [{'id': ..., 'name': ...}, ...].
+    """
+    service = _get_service()
+    images = []
+    page_token = None
+    while True:
+        res = service.files().list(
+            q=f"'{folder_id}' in parents and mimeType contains 'image/' and trashed=false",
+            fields='nextPageToken, files(id, name)',
+            orderBy='name',
+            pageSize=1000,
+            pageToken=page_token,
+            supportsAllDrives=True,
+            includeItemsFromAllDrives=True,
+        ).execute()
+        images.extend(res.get('files', []))
+        page_token = res.get('nextPageToken')
+        if not page_token:
+            break
+    return images
+
+
 def delete_note(file_id):
     """Move a Drive file to trash (silent on error)."""
     try:
```

`mobi/web_album.py`: new file (full contents in Step 2).

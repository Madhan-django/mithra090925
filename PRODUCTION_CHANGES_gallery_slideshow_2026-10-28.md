# PRODUCTION CHANGE GUIDE (Part 2): Gallery Album Slideshow
Date: 28-10-2026
Do this AFTER Part 1 (`PRODUCTION_CHANGES_gallery_2026-10-28.md`).

## What this adds
In Gallery Manage (or PhotoGallery), the admin adds an entry with ONE link. The app then shows all the photos as a slideshow:
swipe left/right, pinch to zoom, "3 / 12" counter, previous/next buttons, a thumbnail strip, and tap to hide the controls.
The first photo is used as the card's cover image (when no thumbnail is set).

| Link pasted by admin | What the app shows |
|---|---|
| Website album page, e.g. `https://jacobindia.edu.in/album.php?slug=independence-day-2026-jnps` | Slideshow of all album photos on that page |
| Web folder (directory listing of images) | Slideshow of all images in that folder |
| Google Drive FOLDER `drive.google.com/drive/folders/...` | Slideshow of all images in the folder |
| Google Drive FILE `drive.google.com/file/d/...` | That image, full screen |
| Direct image URL (`.jpg .jpeg .png .gif .webp .bmp`) | That image, full screen |
| A website page where no photos can be found | Opens the link in the phone's browser |

### How photos are found on a website page (`mobi/web_album.py`)
1. If the page has links to image files (`<a href="....jpg">`, which lightbox galleries and folder listings use), ONLY those are used. They're the full-size photos.
2. Otherwise all `<img>` images on the page are used (lazy-load `data-src`, `data-original` and `srcset` are supported, and the largest size is picked).
3. Images inside `<header>`, `<nav>` and `<footer>`, and logos, icons, social buttons and tiny images (<80px), are skipped.
4. The page must be public (no login). Pages built by JavaScript after loading (no images in the HTML source) can't be read. Those open in the browser instead.
5. Results are cached for 10 minutes (2 minutes if nothing was found).
6. Safety: only http/https links are allowed. localhost and private network addresses are blocked. Timeout is 10 seconds, max page size 5 MB.

## Files changed on the server (4 files)
| File | Change |
|------|--------|
| `mobi/web_album.py` | **NEW FILE**: reads photos from a website album page |
| `lessonplan/drive_utils.py` | NEW function `list_folder_images()` (Drive folders) |
| `mobi/views.py` | 3 new imports, a cover-image block in `PhotoGalleryView`, NEW helpers + NEW class `PhotoAlbumView` |
| `mobi/urls.py` | import `PhotoAlbumView` + 1 new URL `photos/album/` |

No models, no migrations, no new pip packages (only the Python standard library, plus the existing Google Drive client).
New API: `GET /mobi/photos/album/?username=<student>&id=<id from /mobi/photos/>`

---------------------------------------------------------------------

## Drive folder sharing (only for Drive folder links)
Share each album folder: Drive → right-click the folder → Share → General access → **Anyone with the link → Viewer**.
You can also add the service account **mithran-lms-storage@mithran-erp-drive.iam.gserviceaccount.com** as Viewer.
Only images directly inside the folder are shown (not subfolders), sorted by file name.

## Server internet access (for website links)
The production server must be able to open outside websites (outbound HTTP/HTTPS).
Test from the server: open the album link in a browser ON the server. If it loads, this will work.

---------------------------------------------------------------------

## STEP 1: Backup
On the production server, copy these files to a backup folder, e.g. `_backup_slideshow_<date>\`:
- `lessonplan\drive_utils.py`
- `mobi\views.py`
- `mobi\urls.py`
(`mobi\web_album.py` is new, so there's nothing to back up.)

## STEP 2: Check prerequisites
1. Part 1 is already deployed (`PhotoGalleryView` has the `GalleryPhoto` loop that ends with `return Response(data)`).
2. `lessonplan/drive_utils.py` exists with `_get_service()` and `delete_note()` (the Gallery Manage upload uses it).
3. `settings.py` has `GOOGLE_DRIVE_SERVICE_ACCOUNT_FILE`, and the json file is on the server.

## STEP 3: Add the NEW file `mobi/web_album.py`
Copy `mobi/web_album.py` from the dev project into the production `mobi` folder (next to `views.py`).
Full contents, for reference:
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

## STEP 4: `lessonplan/drive_utils.py`: add one function
Find:
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

## STEP 5: `mobi/views.py`: imports
Near the top, find:
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

## STEP 6: `mobi/views.py`: cover image in PhotoGalleryView
Inside `class PhotoGalleryView`, at the END of `get()`, find (this is the end of the Part 1 code):
```python
                'status': 'active',
            })
        return Response(data)
```
Replace with:
```python
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

## STEP 7: `mobi/views.py`: new helpers + PhotoAlbumView
Directly BELOW the end of `PhotoGalleryView` (after its `return Response(data)`), and ABOVE `class VideoGalleryView(APIView):`,
paste this whole block (keep 2 blank lines before and after it):
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
Note: `PhotoGalleryView` uses `_album_images`, which is defined below it. That's fine in Python, because it's looked up when a request comes in.

## STEP 8: `mobi/urls.py`
**8a.** In the `from .views import (...)` block, find:
```python
                    PhotoGalleryView,
```
Change to:
```python
                    PhotoGalleryView, PhotoAlbumView,
```
**8b.** In `urlpatterns`, find:
```python
    path('photos/', PhotoGalleryView.as_view(), name='photos'),
```
Add this line directly BELOW it:
```python
    path('photos/album/', PhotoAlbumView.as_view(), name='photo_album'),
```

## STEP 9: Check for errors
In the project folder with the production venv activated:
```
python -m py_compile mobi\web_album.py
python -m py_compile lessonplan\drive_utils.py
python -m py_compile mobi\views.py
python -m py_compile mobi\urls.py
python manage.py check
```
All should pass with no errors.

Quick check that the server can read a website album (in the venv):
```
python -c "import sys; sys.path.insert(0,'mobi'); import web_album; r=web_album.fetch_album_images('https://jacobindia.edu.in/album.php?slug=independence-day-2026-jnps'); print(len(r)); print(r[:3])"
```
It should print the number of photos found and the first 3 photo URLs.
- `0` → check the page in a browser on the server: does it need a login, does it load photos with JavaScript, or is outbound internet blocked?

## STEP 10: Restart
IIS Manager → Application Pools → the Nexora/Mithran pool → **Recycle** (or restart the service).

## STEP 11: Test
1. Web ERP → Gallery Manage → Add → choose the **link** option → paste `https://jacobindia.edu.in/album.php?slug=independence-day-2026-jnps` → title "Independence Day 2026" → Active → Save.
2. Postman `GET /mobi/photos/?username=<student>` (Bearer token)
   → find the entry. Its `id` looks like `"g12"`, and `PThumbnail` should now be the first photo's URL.
3. Postman `GET /mobi/photos/album/?username=<student>&id=g12`
   → `{"title": "Independence Day 2026", "images": [{id,name,thumb,full}, ...]}` with all the photos.
   - `"images": [], "web_url": ...` → no photos could be read from the page (see Step 9's quick check).
   - `502 Could not read album: ...` → a Drive folder that isn't shared, or a Drive API error.
4. Repeat with a shared Drive folder link.
5. App (new APK): Photo Gallery → tap the card → the slideshow opens with all photos.

Note: albums are cached for 10 minutes. Photos added later appear within 10 minutes, or straight away after an app pool recycle.

---------------------------------------------------------------------

## ANDROID (Mithra app): files in this release
New files:
- `model/AlbumResponse.kt`: `AlbumImage`, `AlbumResponse` (with `web_url`)
- `GallerySlideshow.kt`: slideshow activity (opens `web_url` in the browser if there are no images)
- `SlideAdapter.kt`: ViewPager2 pages (zoomable PhotoView)
- `SlideThumbAdapter.kt`: thumbnail strip
- `res/layout/activity_gallery_slideshow.xml`, `res/layout/item_slide_image.xml`, `res/layout/item_slide_thumb.xml`
- `res/drawable/bg_slide_thumb_selected.xml`

Changed files:
- `GalleryApi.kt`: added `getAlbum()` → `photos/album/`
- `PhotoAdapter.kt`: a Drive folder link or website album link opens `GallerySlideshow`; Drive file / direct image link opens `ImageViewer`; the folder regex also accepts `/drive/u/0/folders/`
- `AndroidManifest.xml`: registered `.GallerySlideshow`
- `app/build.gradle.kts`: added `implementation("androidx.viewpager2:viewpager2:1.0.0")`
- `model/PhotoItem.kt`: from Part 1 (JSON key fix)

Release steps:
1. Gradle sync.
2. `Auth.kt`: switch to the `https://mithran.co.in/...` URLs.
3. Increase `versionCode` / `versionName` (currently 28 / "28.0").
4. Build a signed APK/AAB and publish it.

Order: **deploy the server first, then release the app.**

---------------------------------------------------------------------

## ROLLBACK
1. Put back the backed-up `drive_utils.py`, `views.py` and `urls.py`.
2. Delete (or rename) `mobi\web_album.py`.
3. Recycle the app pool.
No DB changes were made.

## CHECKLIST
- [ ] Part 1 already deployed
- [ ] Backups taken
- [ ] Step 3 `mobi/web_album.py` copied
- [ ] Step 4 `list_folder_images` added to drive_utils.py
- [ ] Step 5 imports (`re`, `hashlib`, `cache`)
- [ ] Step 6 cover block in PhotoGalleryView
- [ ] Step 7 helpers + PhotoAlbumView pasted above VideoGalleryView
- [ ] Step 8 urls.py import + path
- [ ] Step 9 py_compile + manage.py check + web album quick check passed
- [ ] Step 10 app pool recycled
- [ ] Step 11 Postman tests pass (website link + Drive folder)
- [ ] New APK released (production URLs, version bumped)

---------------------------------------------------------------------

## Reference: exact diffs (local dev copy)
```diff
--- lessonplan/drive_utils.py (before)
+++ lessonplan/drive_utils.py (after)
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

```diff
--- mobi/views.py (before)
+++ mobi/views.py (after)
@@ -40,6 +40,9 @@
 from django.utils import timezone
 import calendar
 import os
+import re
+import hashlib
+from django.core.cache import cache
 
 # Create your views here.
 
@@ -454,9 +457,133 @@
                 'Pschool': school_data,
                 'status': 'active',
             })
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
         return Response(data)
 
 
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
+
+
 class VideoGalleryView(APIView):
     authentication_classes = [JWTAuthentication]
     permission_classes = [IsAuthenticated]
```

```diff
--- mobi/urls.py (before)
+++ mobi/urls.py (after)
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

`mobi/web_album.py`: new file (full contents in Step 3).

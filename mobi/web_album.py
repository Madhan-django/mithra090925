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

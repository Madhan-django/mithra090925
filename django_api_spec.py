"""
MITHRAN Android App — Django API Specification
================================================
Two gallery endpoints:

  GET /photos/   → Photo Gallery  (Android: Gallery activity + PhotoAdapter)
  GET /videos/   → Video Gallery  (Android: VideoGallery activity + GalleryAdapter)

Both endpoints require:
  Header : Authorization: Bearer <token>
  Query  : username=<username>

Response : JSON array of items (return [] when none found — never 404)
Auth     : Token-based (DRF TokenAuthentication or JWT)
Access   : Read-only (GET only)
"""

# ──────────────────────────────────────────────────────────────────────────────
# MODELS
# ──────────────────────────────────────────────────────────────────────────────

# models.py

from django.db import models


class School(models.Model):
    """Shared school FK for both photo and video items."""
    name     = models.CharField(max_length=255)
    address  = models.TextField(blank=True)
    email    = models.EmailField(blank=True)
    phone    = models.CharField(max_length=20, blank=True)
    regno    = models.CharField(max_length=50, blank=True)
    logo     = models.URLField(blank=True)
    isactive = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class PhotoGallery(models.Model):
    """
    Photo gallery item.  Endpoint: GET /photos/

    Plink must be a Google Drive URL only (file or folder).
    PThumbnail should be a Drive file URL; Android falls back to Plink if empty.
    """
    STATUS_CHOICES = [("active", "Active"), ("inactive", "Inactive")]

    PTitle     = models.CharField(max_length=255)
    PThumbnail = models.URLField(
        blank=True,
        help_text=(
            "Drive file URL (https://drive.google.com/file/d/<id>/view), "
            "absolute image URL, or relative path (/media/…). "
            "Android extracts the Drive file ID and loads the thumbnail at sz=w600. "
            "Can be left empty when Plink is a Drive file URL — Android uses Plink as fallback."
        )
    )
    Plink      = models.URLField(
        blank=True,
        help_text=(
            "Google Drive URL only — either a single image file or an album folder:\n"
            "  • Drive file   : https://drive.google.com/file/d/<id>/view\n"
            "  • Drive folder : https://drive.google.com/drive/folders/<id>"
        )
    )
    Pdesc      = models.TextField(blank=True)
    Pdate      = models.DateField(null=True, blank=True, help_text="Date the photos were taken")
    Ppostdate  = models.DateField(auto_now_add=True, help_text="Date posted to the app")
    Pschool    = models.ForeignKey(School, on_delete=models.CASCADE, related_name="photos")
    status     = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")

    class Meta:
        ordering = ["-Ppostdate"]

    def __str__(self):
        return self.PTitle


class VideoGallery(models.Model):
    """
    Video gallery item.  Endpoint: GET /videos/

    Vlink must be a YouTube URL or a Google Drive URL (file or folder).
    VThumbnail can be left empty for YouTube items — Android auto-generates it.
    """
    STATUS_CHOICES = [("active", "Active"), ("inactive", "Inactive")]

    VTitle     = models.CharField(max_length=255)
    VThumbnail = models.URLField(
        blank=True,
        help_text=(
            "Drive file URL, absolute URL, or relative path. "
            "For YouTube Vlinks leave this empty — Android auto-fetches "
            "https://img.youtube.com/vi/<id>/hqdefault.jpg. "
            "For Drive Vlinks provide a Drive file URL as the thumbnail."
        )
    )
    Vlink      = models.URLField(
        blank=True,
        help_text=(
            "YouTube or Google Drive URL only:\n"
            "  • YouTube watch  : https://www.youtube.com/watch?v=<id>\n"
            "  • YouTube short  : https://www.youtube.com/shorts/<id>\n"
            "  • YouTube embed  : https://www.youtube.com/embed/<id>\n"
            "  • youtu.be short : https://youtu.be/<id>\n"
            "  • Drive file     : https://drive.google.com/file/d/<id>/view\n"
            "  • Drive folder   : https://drive.google.com/drive/folders/<id>"
        )
    )
    Vdesc      = models.TextField(blank=True)
    Vdate      = models.DateField(null=True, blank=True, help_text="Date the video was recorded")
    Vpostdate  = models.DateField(auto_now_add=True, help_text="Date posted to the app")
    Vschool    = models.ForeignKey(School, on_delete=models.CASCADE, related_name="videos")
    status     = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")

    class Meta:
        ordering = ["-Vpostdate"]

    def __str__(self):
        return self.VTitle


# ──────────────────────────────────────────────────────────────────────────────
# SERIALIZERS
# ──────────────────────────────────────────────────────────────────────────────

# serializers.py

from rest_framework import serializers
# from .models import School, PhotoGallery, VideoGallery  # uncomment in real project


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model  = School
        fields = ["id", "name", "address", "email", "phone", "regno", "logo", "isactive"]


class PhotoGallerySerializer(serializers.ModelSerializer):
    Pschool = SchoolSerializer(read_only=True)

    class Meta:
        model  = PhotoGallery
        fields = [
            "id", "PTitle", "PThumbnail", "Plink",
            "Pdesc", "Pdate", "Ppostdate", "Pschool", "status",
        ]


class VideoGallerySerializer(serializers.ModelSerializer):
    Vschool = SchoolSerializer(read_only=True)

    class Meta:
        model  = VideoGallery
        fields = [
            "id", "VTitle", "VThumbnail", "Vlink",
            "Vdesc", "Vdate", "Vpostdate", "Vschool", "status",
        ]


# ──────────────────────────────────────────────────────────────────────────────
# VIEWS
# ──────────────────────────────────────────────────────────────────────────────

# views.py

from rest_framework.views import APIView
from rest_framework.response import Response as DRFResponse
from rest_framework.permissions import IsAuthenticated
# from .models import PhotoGallery, VideoGallery
# from .serializers import PhotoGallerySerializer, VideoGallerySerializer


class PhotoGalleryView(APIView):
    """
    GET /photos/?username=<username>
    Returns all active photos for the school linked to the given student.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.query_params.get("username", "")
        photos = PhotoGallery.objects.filter(
            status="active",
            Pschool__students__username=username  # adjust FK path to match your schema
        ).select_related("Pschool")
        serializer = PhotoGallerySerializer(photos, many=True)
        return DRFResponse(serializer.data)


class VideoGalleryView(APIView):
    """
    GET /videos/?username=<username>
    Returns all active videos for the school linked to the given student.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.query_params.get("username", "")
        videos = VideoGallery.objects.filter(
            status="active",
            Vschool__students__username=username  # adjust FK path to match your schema
        ).select_related("Vschool")
        serializer = VideoGallerySerializer(videos, many=True)
        return DRFResponse(serializer.data)


# ──────────────────────────────────────────────────────────────────────────────
# URLS
# ──────────────────────────────────────────────────────────────────────────────

# urls.py  (add to your app's urlpatterns)

from django.urls import path
# from .views import PhotoGalleryView, VideoGalleryView

urlpatterns_gallery = [
    path("photos/", PhotoGalleryView.as_view(), name="photo-gallery"),
    path("videos/", VideoGalleryView.as_view(), name="video-gallery"),
]


# ──────────────────────────────────────────────────────────────────────────────
# JSON RESPONSE EXAMPLES
# ──────────────────────────────────────────────────────────────────────────────

# ── /photos/ — example responses ─────────────────────────────────────────────

PHOTO_RESPONSE_EXAMPLE = [
    {
        # Album: Plink is a Drive folder → Android opens the folder in the browser.
        # PThumbnail is a Drive file URL → Android uses its file ID for the grid thumbnail.
        "id": 1,
        "PTitle": "Sports Day 2024",
        "PThumbnail": "https://drive.google.com/file/d/1AbCdEfGhIjKlMn/view",
        "Plink": "https://drive.google.com/drive/folders/1aBcDeFgHiJkLmN",
        "Pdesc": "Annual sports day highlights",
        "Pdate": "2024-01-20",
        "Ppostdate": "2024-01-21",
        "Pschool": {
            "id": 1, "name": "Nexis School", "address": "Chennai, TN",
            "email": "admin@nexis.edu", "phone": "9876543210",
            "regno": "TN12345", "logo": "https://mithran.co.in/media/logos/school.png",
            "isactive": True
        },
        "status": "active"
    },
    {
        # Single image: Plink is a Drive file → Android opens it full-screen in ImageViewer.
        # PThumbnail is the same URL — Android reuses it for the grid thumbnail.
        "id": 2,
        "PTitle": "Science Exhibition",
        "PThumbnail": "https://drive.google.com/file/d/2XyZaBcDeFgHiJkL/view",
        "Plink": "https://drive.google.com/file/d/2XyZaBcDeFgHiJkL/view",
        "Pdesc": "Students showcase projects",
        "Pdate": "2024-03-10",
        "Ppostdate": "2024-03-11",
        "Pschool": {
            "id": 1, "name": "Nexis School", "address": "Chennai, TN",
            "email": "admin@nexis.edu", "phone": "9876543210",
            "regno": "TN12345", "logo": "https://mithran.co.in/media/logos/school.png",
            "isactive": True
        },
        "status": "active"
    },
]

# ── /videos/ — example responses ─────────────────────────────────────────────

VIDEO_RESPONSE_EXAMPLE = [
    {
        # YouTube link: VThumbnail is empty.
        # Android extracts the video ID from Vlink and auto-loads the YouTube thumbnail:
        #   https://img.youtube.com/vi/dQw4w9WgXcQ/hqdefault.jpg
        # On tap: opens in VideoPlayer → redirects to the YouTube app / browser.
        "id": 1,
        "VTitle": "Annual Day Performance",
        "VThumbnail": "",
        "Vlink": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "Vdesc": "Cultural performances from Annual Day",
        "Vdate": "2024-02-15",
        "Vpostdate": "2024-02-16",
        "Vschool": {
            "id": 1, "name": "Nexis School", "address": "Chennai, TN",
            "email": "admin@nexis.edu", "phone": "9876543210",
            "regno": "TN12345", "logo": "https://mithran.co.in/media/logos/school.png",
            "isactive": True
        },
        "status": "active"
    },
    {
        # YouTube short: same auto-thumbnail behaviour as above.
        "id": 2,
        "VTitle": "Independence Day Highlights",
        "VThumbnail": "",
        "Vlink": "https://www.youtube.com/shorts/abcde12345f",
        "Vdesc": "Independence Day short clip",
        "Vdate": "2024-08-15",
        "Vpostdate": "2024-08-16",
        "Vschool": {
            "id": 1, "name": "Nexis School", "address": "Chennai, TN",
            "email": "admin@nexis.edu", "phone": "9876543210",
            "regno": "TN12345", "logo": "https://mithran.co.in/media/logos/school.png",
            "isactive": True
        },
        "status": "active"
    },
    {
        # Drive file: VThumbnail is a Drive file URL for the cover frame.
        # Android extracts the file ID and loads the thumbnail at sz=w600.
        # On tap: opens in the browser (Drive video playback requires Google auth).
        "id": 3,
        "VTitle": "Republic Day Celebration",
        "VThumbnail": "https://drive.google.com/file/d/1ThumbDriveFileId/view",
        "Vlink": "https://drive.google.com/file/d/1VideoDriveFileId/view",
        "Vdesc": "Republic Day flag hoisting ceremony",
        "Vdate": "2024-01-26",
        "Vpostdate": "2024-01-27",
        "Vschool": {
            "id": 1, "name": "Nexis School", "address": "Chennai, TN",
            "email": "admin@nexis.edu", "phone": "9876543210",
            "regno": "TN12345", "logo": "https://mithran.co.in/media/logos/school.png",
            "isactive": True
        },
        "status": "active"
    },
    {
        # Drive folder: contains multiple videos.
        # On tap: opens the Drive folder in the browser.
        "id": 4,
        "VTitle": "Sports Meet 2024",
        "VThumbnail": "https://drive.google.com/file/d/1FolderCoverThumbId/view",
        "Vlink": "https://drive.google.com/drive/folders/1SportsMeetFolderId",
        "Vdesc": "Full sports meet video collection",
        "Vdate": "2024-04-05",
        "Vpostdate": "2024-04-06",
        "Vschool": {
            "id": 1, "name": "Nexis School", "address": "Chennai, TN",
            "email": "admin@nexis.edu", "phone": "9876543210",
            "regno": "TN12345", "logo": "https://mithran.co.in/media/logos/school.png",
            "isactive": True
        },
        "status": "active"
    },
]


# ──────────────────────────────────────────────────────────────────────────────
# ANDROID ADAPTER BEHAVIOUR — REFERENCE FOR DJANGO DEVELOPER
# ──────────────────────────────────────────────────────────────────────────────
#
# ┌─────────────────────────────────────────────────────────────────────────────┐
# │  PHOTO GALLERY  (PhotoAdapter.kt)  —  GET /photos/                         │
# ├──────────────────┬──────────────────────────────────────────────────────────┤
# │  Plink value     │  What Android does on tap                                │
# ├──────────────────┼──────────────────────────────────────────────────────────┤
# │  Drive file URL  │  Opens full-screen in the in-app ImageViewer             │
# │                  │  (loads https://drive.google.com/thumbnail?id=<id>&sz=w2048) │
# │  Drive folder URL│  Opens Google Drive folder in the browser                │
# └──────────────────┴──────────────────────────────────────────────────────────┘
#
# PThumbnail resolution order (Android picks the first match):
#   1. PThumbnail contains a Drive file URL  → Drive thumbnail API at sz=w600
#   2. PThumbnail starts with "http"         → use as-is
#   3. PThumbnail is a non-empty string      → prefix with https://mithran.co.in
#   4. PThumbnail is empty + Plink is Drive file   → Drive thumbnail of Plink file
#   5. PThumbnail is empty + Plink is Drive folder → Drive thumbnail of folder ID
#      (folders may not have a thumbnail — prefer setting PThumbnail explicitly)
#   6. No match                              → no thumbnail shown
#
# ┌─────────────────────────────────────────────────────────────────────────────┐
# │  VIDEO GALLERY  (GalleryAdapter.kt)  —  GET /videos/                       │
# ├──────────────────┬──────────────────────────────────────────────────────────┤
# │  Vlink value     │  What Android does on tap                                │
# ├──────────────────┼──────────────────────────────────────────────────────────┤
# │  YouTube URL     │  Opens VideoPlayer → redirects to YouTube app / browser  │
# │  Drive file URL  │  Opens in the browser (Drive requires Google auth)        │
# │  Drive folder URL│  Opens Google Drive folder in the browser                │
# └──────────────────┴──────────────────────────────────────────────────────────┘
#
# Supported YouTube URL formats (all redirect to the YouTube app):
#   https://www.youtube.com/watch?v=<11-char-id>
#   https://www.youtube.com/shorts/<11-char-id>
#   https://www.youtube.com/embed/<11-char-id>
#   https://youtu.be/<11-char-id>
#
# VThumbnail resolution order (Android picks the first match):
#   1. VThumbnail contains a Drive file URL  → Drive thumbnail API at sz=w600
#   2. VThumbnail starts with "http"         → use as-is
#   3. VThumbnail is a non-empty string      → prefix with https://mithran.co.in
#   4. VThumbnail is empty + Vlink is YouTube → auto-fetch YouTube thumbnail:
#      https://img.youtube.com/vi/<id>/hqdefault.jpg   ← leave VThumbnail empty for YouTube
#   5. VThumbnail is empty + Vlink is Drive file   → Drive thumbnail of Vlink file
#   6. VThumbnail is empty + Vlink is Drive folder → Drive thumbnail of folder ID
#   7. No match                              → no thumbnail shown
#
# ──────────────────────────────────────────────────────────────────────────────
# RECOMMENDED PATTERNS FOR ADMIN DATA ENTRY
# ──────────────────────────────────────────────────────────────────────────────
#
#  Photo — single image:
#    Plink      = https://drive.google.com/file/d/<image-id>/view
#    PThumbnail = (same as Plink — or leave empty, Android will use Plink)
#
#  Photo — album folder:
#    Plink      = https://drive.google.com/drive/folders/<folder-id>
#    PThumbnail = https://drive.google.com/file/d/<cover-image-id>/view
#                 (pick any image from the folder as the cover)
#
#  Video — YouTube:
#    Vlink      = https://www.youtube.com/watch?v=<id>   (or shorts / youtu.be)
#    VThumbnail = (leave empty — Android generates it automatically)
#
#  Video — Drive file:
#    Vlink      = https://drive.google.com/file/d/<video-id>/view
#    VThumbnail = https://drive.google.com/file/d/<thumbnail-image-id>/view
#                 (upload a cover-frame image to Drive and use its URL)
#
#  Video — Drive folder:
#    Vlink      = https://drive.google.com/drive/folders/<folder-id>
#    VThumbnail = https://drive.google.com/file/d/<cover-image-id>/view

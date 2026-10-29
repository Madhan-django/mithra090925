"""
Management command: create_sample_banners

Creates one "Admissions Open" sample banner for every school that does not
already have any banners.  The banner image is generated with Pillow so no
external file is needed.

Usage:
    python manage.py create_sample_banners
    python manage.py create_sample_banners --force   # recreate even if banners exist
"""
import io
import os
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from institutions.models import school
from mobi.models import Banner


def _draw_banner(school_name: str) -> bytes:
    from PIL import Image, ImageDraw, ImageFont

    W, H = 1200, 400
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)

    # ── gradient background (indigo → purple) ──────────────────────────
    for y in range(H):
        r = int(79  + (126 - 79)  * y / H)
        g = int(70  + (34  - 70)  * y / H)
        b = int(229 + (197 - 229) * y / H)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # ── decorative circles ──────────────────────────────────────────────
    draw.ellipse([980, -60, 1160, 120],  fill=(255, 255, 255, 0), outline=(255, 255, 255, 30), width=2)
    draw.ellipse([1060, 280, 1210, 430], fill=(255, 255, 255, 0), outline=(255, 255, 255, 20), width=2)

    # ── try to use a system font, fall back to default ──────────────────
    def _font(size):
        for path in [
            "C:/Windows/Fonts/arialbd.ttf",
            "C:/Windows/Fonts/arial.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ]:
            if os.path.exists(path):
                try:
                    return ImageFont.truetype(path, size)
                except Exception:
                    pass
        return ImageFont.load_default()

    # ── badge pill ──────────────────────────────────────────────────────
    badge_text = "ADMISSIONS OPEN"
    badge_font = _font(22)
    # pill background
    draw.rounded_rectangle([60, 60, 300, 100], radius=18, fill=(255, 255, 255, 50))
    draw.text((75, 68), badge_text, font=badge_font, fill=(255, 255, 255))

    # ── school name ─────────────────────────────────────────────────────
    sch_font = _font(38)
    draw.text((60, 120), school_name, font=sch_font, fill=(255, 255, 255))

    # ── headline ────────────────────────────────────────────────────────
    head_font = _font(56)
    draw.text((60, 178), "Enrol for 2025 – 26", font=head_font, fill=(255, 255, 255))

    # ── sub-text ─────────────────────────────────────────────────────────
    sub_font = _font(28)
    draw.text((60, 258), "Secure your child's future today", font=sub_font, fill=(199, 210, 254))

    # ── CTA button shape ────────────────────────────────────────────────
    draw.rounded_rectangle([60, 310, 290, 360], radius=24, fill=(255, 255, 255))
    btn_font = _font(24)
    draw.text((100, 322), "Apply Now  →", font=btn_font, fill=(79, 70, 229))

    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return buf.getvalue()


class Command(BaseCommand):
    help = "Create a sample Admissions Open banner for each school"

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Add sample banner even if the school already has banners",
        )

    def handle(self, *args, **options):
        schools = school.objects.all()
        if not schools.exists():
            self.stdout.write(self.style.WARNING("No schools found in the database."))
            return

        created = 0
        skipped = 0

        for sch in schools:
            if not options["force"] and Banner.objects.filter(school_name=sch).exists():
                self.stdout.write(f"  SKIP  {sch.name}  (already has banners)")
                skipped += 1
                continue

            try:
                img_bytes = _draw_banner(sch.name)
            except Exception as exc:
                self.stdout.write(self.style.ERROR(f"  ERROR drawing banner for {sch.name}: {exc}"))
                continue

            safe_name = sch.name.replace(" ", "_").lower()
            filename = f"sample_admission_{safe_name}.png"

            banner = Banner(
                school_name=sch,
                title=f"Admissions Open 2025-26 — {sch.name}",
                link_url="",
                is_active=True,
                display_order=0,
            )
            banner.image.save(filename, ContentFile(img_bytes), save=True)

            self.stdout.write(self.style.SUCCESS(f"  CREATED  {sch.name}  =>  {banner.image.name}"))
            created += 1

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(f"Done — {created} banner(s) created, {skipped} skipped."))

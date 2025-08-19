import os
import requests
from django.conf import settings
from PIL import ImageFont

FONTS_DIR = os.path.join(settings.BASE_DIR, "fonts_cache")
os.makedirs(FONTS_DIR, exist_ok=True)

GOOGLE_FONTS_BASE = "https://github.com/google/fonts/raw/main/ofl/"

def get_google_font(font_name: str, weight: str = "Regular", size: int = 40):
    """
    Fetch a Google Font .ttf from GitHub if not cached, and return a PIL ImageFont.
    """
    font_folder = font_name.lower().replace(" ", "")
    file_name = f"{font_name.replace(' ', '')}-{weight}.ttf"
    font_path = os.path.join(FONTS_DIR, file_name)

    if not os.path.exists(font_path):
        url = f"{GOOGLE_FONTS_BASE}{font_folder}/{file_name}"
        r = requests.get(url)
        if r.status_code == 200:
            with open(font_path, "wb") as f:
                f.write(r.content)
        else:
            return ImageFont.load_default()  # fallback

    return ImageFont.truetype(font_path, size)


def get_badge_fonts():
    """Load all fonts defined in settings.BADGE_FONT"""
    config = getattr(settings, "BADGE_FONT", {})
    family = config.get("family", "Poppins")
    weights = config.get("weights", {})
    sizes = config.get("sizes", {})

    return {
        name: get_google_font(family, weights.get(name, "Regular"), sizes.get(name, 40))
        for name in ["title", "subtitle", "name", "course", "score", "footer"]
    }

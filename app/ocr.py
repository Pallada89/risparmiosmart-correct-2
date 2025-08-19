
import pytesseract
from PIL import Image, ImageFilter, ImageOps
import io
import re
from typing import List, Tuple
from .schemas import OfferCreate

def preprocess_image(img: Image.Image) -> Image.Image:
    # Convert to grayscale, increase contrast, apply sharpen
    gray = ImageOps.grayscale(img)
    gray = ImageOps.autocontrast(gray)
    sharpened = gray.filter(ImageFilter.SHARPEN)
    return sharpened

def extract_text(file_bytes: bytes, lang: str = "ita") -> str:
    img = Image.open(io.BytesIO(file_bytes)).convert("RGB")
    img = preprocess_image(img)
    text = pytesseract.image_to_string(img, lang=lang)
    return text

# Very simple parser: find lines with product + price pattern
PRICE_PAT = re.compile(r"""
    (?P<name>[A-Za-zÀ-ÿ0-9'\-\s]{3,}?)
    [\s,:-]*
    (?P<price>\d+[\.,]?\d*)\s*(?:€|EUR)
""", re.VERBOSE)

def parse_offers(raw_text: str, supermarket: str = "") -> List[OfferCreate]:
    offers = []
    for m in PRICE_PAT.finditer(raw_text):
        name = m.group("name").strip()
        price = m.group("price").replace(",", ".")
        try:
            price_val = float(price)
        except ValueError:
            continue
        # try to extract quantity if present at end of name (e.g., "500g", "1L")
        qty_match = re.search(r"(\b\d+\s?(?:g|kg|ml|l|pz|pezzi)\b)", name, re.IGNORECASE)
        quantity = qty_match.group(1) if qty_match else None
        offers.append(OfferCreate(
            supermarket=supermarket or "unknown",
            product_name=name,
            quantity=quantity,
            price=price_val,
            currency="EUR",
            source="ocr",
            raw_text=raw_text[:1000]  # store a snippet
        ))
    return offers

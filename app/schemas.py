
from pydantic import BaseModel
from typing import Optional, List

class OfferCreate(BaseModel):
    supermarket: str
    product_name: str
    quantity: Optional[str] = None
    price: float
    currency: str = "EUR"
    valid_until: Optional[str] = None
    source: Optional[str] = None
    raw_text: Optional[str] = None

class OfferRead(OfferCreate):
    id: int

    class Config:
        from_attributes = True

class OCRResult(BaseModel):
    text: str
    offers: List[OfferCreate] = []

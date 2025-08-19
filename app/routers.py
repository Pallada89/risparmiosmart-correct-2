
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi import Query
from sqlalchemy.orm import Session
from typing import List, Optional
from .database import get_db
from . import models
from .schemas import OfferCreate, OfferRead
from .ocr import extract_text, parse_offers

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok"}

@router.post("/ocr", response_model=dict)
async def ocr_endpoint(
    file: UploadFile = File(...),
    supermarket: Optional[str] = None,
    db: Session = Depends(get_db)
):
    if not file:
        raise HTTPException(status_code=400, detail="File mancante")
    content = await file.read()
    try:
        text = extract_text(content, lang="ita")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR error: {e}")
    # parse and persist
    offers = parse_offers(text, supermarket=supermarket or "")
    for o in offers:
        db_offer = models.Offer(
            supermarket=o.supermarket,
            product_name=o.product_name,
            quantity=o.quantity,
            price=o.price,
            currency=o.currency,
            valid_until=o.valid_until,
            source=o.source,
            raw_text=o.raw_text
        )
        db.add(db_offer)
    db.commit()
    return {"text": text, "offers_extracted": len(offers)}

@router.post("/offers", response_model=OfferRead)
def create_offer(payload: OfferCreate, db: Session = Depends(get_db)):
    obj = models.Offer(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/offers", response_model=List[OfferRead])
def list_offers(
    db: Session = Depends(get_db),
    q: Optional[str] = Query(None, description="testo da cercare nel nome prodotto"),
    supermarket: Optional[str] = Query(None),
    limit: int = 50
):
    query = db.query(models.Offer)
    if q:
        query = query.filter(models.Offer.product_name.ilike(f"%{q}%"))
    if supermarket:
        query = query.filter(models.Offer.supermarket.ilike(f"%{supermarket}%"))
    query = query.order_by(models.Offer.created_at.desc()).limit(min(limit, 200))
    return query.all()

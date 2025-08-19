
from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.sql import func
from .database import Base

class Offer(Base):
    __tablename__ = "offers"
    id = Column(Integer, primary_key=True, index=True)
    supermarket = Column(String(120), index=True)
    product_name = Column(String(255), index=True)
    quantity = Column(String(50), nullable=True)
    price = Column(Float, index=True)
    currency = Column(String(10), default="EUR")
    valid_until = Column(String(50), nullable=True)
    source = Column(String(255), nullable=True)  # es. "ocr" / "scraper"
    raw_text = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

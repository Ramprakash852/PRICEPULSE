from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.engine.url import make_url
from sqlalchemy.exc import ArgumentError
from dotenv import load_dotenv
from datetime import datetime
from app.utils.logger import logger
import os
from pathlib import Path

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def build_default_database_url() -> str:
    db_path = Path(__file__).resolve().parent / "pricepulse.sqlite3"
    return f"sqlite:///{db_path.as_posix()}"

def normalize_database_url(raw_url: str) -> str:
    url = raw_url.strip().strip('"').strip("'")

    # Handle accidental copy/paste formats like: DATABASE_URL=postgresql://...
    if url.lower().startswith("database_url="):
        url = url.split("=", 1)[1].strip()

    # Normalize older provider format for SQLAlchemy compatibility.
    if url.startswith("postgres://"):
        url = "postgresql://" + url[len("postgres://"):]

    return url


DATABASE_URL = normalize_database_url(DATABASE_URL or "")

try:
    make_url(DATABASE_URL)
except ArgumentError as exc:
    logger.warning("Invalid DATABASE_URL format. Falling back to local SQLite database.")
    DATABASE_URL = build_default_database_url()

engine = create_engine(DATABASE_URL)

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True, nullable=False)
    price = Column(Float)
    availability = Column(String)
    rating = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationship to price history
    price_history = relationship("PriceHistory", back_populates="product")

class PriceHistory(Base):
    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    price = Column(Float, nullable=False)
    recorded_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationship back to product
    product = relationship("Product", back_populates="price_history")

Base.metadata.create_all(engine)

logger.info("✓ Database tables created successfully!")
logger.info("Tables: products, price_history")
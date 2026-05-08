from fastapi import FastAPI, Query
from sqlalchemy.orm import sessionmaker
from app.database.models import Product, PriceHistory, engine, Base
from app.utils.logger import logger
from app.api.schemas import (
    ProductResponse, 
    ProductDetailResponse, 
    HealthResponse, 
    SearchResponse,
    PriceSnapshot
)
from typing import List

app = FastAPI(
    title="PricePulse API",
    description="Competitor Price Intelligence Platform",
    version="1.0.0"
)

Session = sessionmaker(bind=engine)

@app.on_event("startup")
def startup_event():
    """Initialize database tables on API startup"""
    try:
        Base.metadata.create_all(engine)
        logger.info("✓ Database tables initialized on startup")
    except Exception as e:
        logger.error(f"Failed to initialize database tables: {e}")

@app.get("/health", response_model=HealthResponse)
def health():
    """Health check endpoint - returns service status"""
    logger.info("Health check endpoint called")
    return {
        "status": "healthy",
        "message": "PricePulse API is running"
    }

@app.get("/", response_model=dict)
def home():
    """Home endpoint - returns welcome message"""
    logger.info("Home endpoint called")
    return {"message": "PricePulse API Running"}

@app.get("/products", response_model=List[ProductResponse])
def get_products():
    """Retrieve all products from the database"""
    logger.info("Fetching all products")
    session = Session()

    try:
        products = session.query(Product).all()
        logger.info(f"Retrieved {len(products)} products")
        return products
    
    finally:
        session.close()

@app.get("/top-rated", response_model=List[ProductResponse])
def top_rated():
    """Retrieve top-rated products (rating >= 4)"""
    logger.info("Fetching top-rated products")
    session = Session()

    try:
        products = session.query(Product).filter(Product.rating >= 4).all()
        logger.info(f"Retrieved {len(products)} top-rated products")
        return products
    
    finally:
        session.close()

@app.get("/search", response_model=SearchResponse)
def search_product(name: str = Query(..., min_length=1, description="Product name to search for")):
    """Search for products by name (case-insensitive)"""
    logger.info(f"Searching for products with name containing: {name}")
    session = Session()

    try:
        # Search using case-insensitive LIKE query
        products = session.query(Product).filter(
            Product.title.ilike(f"%{name}%")
        ).all()
        
        logger.info(f"Search found {len(products)} results for '{name}'")

        return {
            "total_results": len(products),
            "products": products
        }
    
    finally:
        session.close()

@app.get("/top-discounts", response_model=List[ProductResponse])
def top_discounts(limit: int = Query(10, ge=1, le=100, description="Number of results to return")):
    """Retrieve products with the lowest prices (top discounts)"""
    logger.info(f"Fetching top {limit} discounted products")
    session = Session()

    try:
        products = session.query(Product).order_by(Product.price.asc()).limit(limit).all()
        logger.info(f"Retrieved {len(products)} discounted products")
        return products
    
    finally:
        session.close()

@app.get("/products/{product_id}/price-history", response_model=ProductDetailResponse)
def get_price_history(product_id: int):
    """Retrieve detailed product information including price history"""
    logger.info(f"Fetching price history for product {product_id}")
    session = Session()

    try:
        product = session.query(Product).filter_by(id=product_id).first()
        
        if not product:
            logger.warning(f"Product {product_id} not found")
            return {"error": "Product not found"}

        price_history = session.query(PriceHistory).filter_by(product_id=product_id).order_by(PriceHistory.recorded_at).all()
        logger.info(f"Retrieved {len(price_history)} price snapshots for product {product_id}")

        return product
    
    finally:
        session.close()
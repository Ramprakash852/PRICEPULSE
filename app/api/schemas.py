from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class PriceSnapshot(BaseModel):
    price: float
    recorded_at: datetime

class ProductResponse(BaseModel):
    id: int
    title: str
    price: float
    availability: str
    rating: int
    created_at: datetime

    class Config:
        from_attributes = True

class ProductDetailResponse(BaseModel):
    id: int
    title: str
    price: float
    availability: str
    rating: int
    created_at: datetime
    price_history: List[PriceSnapshot]

    class Config:
        from_attributes = True

class HealthResponse(BaseModel):
    status: str
    message: str

class SearchResponse(BaseModel):
    total_results: int
    products: List[ProductResponse]

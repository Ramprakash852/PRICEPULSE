from fastapi import FastAPI
from sqlalchemy.orm import sessionmaker
from app.database.models import Product, engine

app = FastAPI()

Session = sessionmaker(bind=engine)

@app.get("/")
def home():
    return {"message": "PricePulse API Running"}

@app.get("/products")
def get_products():

    session = Session()

    products = session.query(Product).all()

    result = []

    for product in products:
        result.append({
            "id": product.id,
            "title": product.title,
            "price": product.price,
            "availability": product.availability,
            "rating": product.rating
        })

    return result

@app.get("/top-rated")
def top_rated():

    session = Session()

    products = session.query(Product).filter(Product.rating >= 4).all()

    result = []

    for product in products:
        result.append({
            "title": product.title,
            "price": product.price,
            "rating": product.rating
        })

    return result
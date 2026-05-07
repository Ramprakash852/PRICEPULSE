import pandas as pd
from sqlalchemy.orm import sessionmaker
from app.database.models import Product, engine

Session = sessionmaker(bind=engine)
session = Session()

df = pd.read_csv("app/cleaning/cleaned_data.csv")

for _, row in df.iterrows():

    existing_product = session.query(Product).filter_by(title=row["title"]).first()

    if not existing_product:
        product = Product(
            title=row["title"],
            price=row["price"],
            availability=row["availability"],
            rating=row["rating"]
        )

        session.add(product)

session.commit()

print("Data inserted successfully!")
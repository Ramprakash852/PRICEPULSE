import pandas as pd
from sqlalchemy.orm import sessionmaker
from app.database.models import Product, PriceHistory, engine
from app.utils.logger import logger

Session = sessionmaker(bind=engine)
session = Session()

logger.info("Loading cleaned data...")
df = pd.read_csv("app/cleaning/cleaned_data.csv")

new_products_count = 0
updated_products_count = 0
price_snapshots_recorded = 0

for _, row in df.iterrows():

    existing_product = session.query(Product).filter_by(title=row["title"]).first()

    if not existing_product:
        # Create new product
        product = Product(
            title=row["title"],
            price=row["price"],
            availability=row["availability"],
            rating=row["rating"]
        )
        session.add(product)
        session.flush()  # Flush to get the product ID
        
        # Record initial price in history
        price_snapshot = PriceHistory(
            product_id=product.id,
            price=row["price"]
        )
        session.add(price_snapshot)
        new_products_count += 1
        price_snapshots_recorded += 1
        logger.info(f"New product added: {row['title']} (${row['price']})")

    else:
        # Update existing product and record price change
        if existing_product.price != row["price"]:
            logger.info(f"Price change detected for {row['title']}: ${existing_product.price} → ${row['price']}")
            existing_product.price = row["price"]
            existing_product.availability = row["availability"]
            existing_product.rating = row["rating"]
            
            # Record price snapshot
            price_snapshot = PriceHistory(
                product_id=existing_product.id,
                price=row["price"]
            )
            session.add(price_snapshot)
            price_snapshots_recorded += 1
            updated_products_count += 1

session.commit()
session.close()

logger.info("\n=== DATA INSERT SUMMARY ===")
logger.info(f"New products inserted: {new_products_count}")
logger.info(f"Existing products updated: {updated_products_count}")
logger.info(f"Price snapshots recorded: {price_snapshots_recorded}")
logger.info("===========================\n")

logger.info("✓ Data insertion completed successfully!")
"""
Database Migration Utility
Handles database schema updates without losing data
"""

import os
import sys

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from sqlalchemy import text, inspect
from app.utils.logger import logger
from app.database.models import engine, Base, Product, PriceHistory

def check_table_exists(table_name):
    """Check if a table exists in the database"""
    inspector = inspect(engine)
    return table_name in inspector.get_table_names()

def check_column_exists(table_name, column_name):
    """Check if a column exists in a table"""
    inspector = inspect(engine)
    if not check_table_exists(table_name):
        return False
    columns = [col['name'] for col in inspector.get_columns(table_name)]
    return column_name in columns

def migrate_schema():
    """
    Migrate database schema to match current models
    Handles adding missing columns and tables
    """
    
    logger.info("=" * 80)
    logger.info("🔄 STARTING DATABASE MIGRATION")
    logger.info("=" * 80)
    
    with engine.begin() as connection:
        
        # ========== CREATE MISSING TABLES ==========
        logger.info("\n📋 Checking tables...")
        
        # Check if price_history table exists
        if not check_table_exists("price_history"):
            logger.info("❌ price_history table missing - creating...")
            try:
                # Create price_history table
                PriceHistory.__table__.create(engine, checkfirst=True)
                logger.info("✅ Created price_history table")
            except Exception as e:
                logger.error(f"Failed to create price_history table: {e}")
                return False
        else:
            logger.info("✅ price_history table exists")
        
        # ========== ADD MISSING COLUMNS ==========
        logger.info("\n🔧 Checking columns in products table...")
        
        # Check created_at column
        if check_table_exists("products"):
            if not check_column_exists("products", "created_at"):
                logger.info("❌ created_at column missing - adding...")
                try:
                    connection.execute(text(
                        "ALTER TABLE products ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
                    ))
                    connection.commit()
                    logger.info("✅ Added created_at column to products table")
                except Exception as e:
                    logger.error(f"Failed to add created_at column: {e}")
                    return False
            else:
                logger.info("✅ created_at column exists")
            
            # Check title unique constraint
            logger.info("Checking unique constraint on title...")
            inspector = inspect(engine)
            constraints = [const['name'] for const in inspector.get_unique_constraints("products")]
            
            if not any("title" in str(const) for const in constraints):
                logger.warning("⚠️  title unique constraint missing")
                logger.info("Note: Run 'ALTER TABLE products ADD CONSTRAINT products_title_unique UNIQUE (title)' manually if needed")
            else:
                logger.info("✅ title constraint exists")
    
    logger.info("\n" + "=" * 80)
    logger.info("✅ DATABASE MIGRATION COMPLETED")
    logger.info("=" * 80 + "\n")
    return True

def recreate_all_tables():
    """
    Drop all tables and recreate them
    WARNING: This will delete all data!
    """
    
    response = input(
        "\n⚠️  WARNING: This will DELETE all data in the database!\n"
        "Type 'DELETE ALL' to confirm: "
    )
    
    if response != "DELETE ALL":
        logger.info("Migration cancelled")
        return False
    
    logger.info("=" * 80)
    logger.info("🗑️  DROPPING ALL TABLES")
    logger.info("=" * 80)
    
    try:
        Base.metadata.drop_all(engine)
        logger.info("✅ All tables dropped")
        
        logger.info("\n🔨 CREATING NEW TABLES")
        Base.metadata.create_all(engine)
        logger.info("✅ All tables created with new schema")
        
        logger.info("\n" + "=" * 80)
        logger.info("✅ DATABASE RECREATION COMPLETED")
        logger.info("=" * 80 + "\n")
        return True
    
    except Exception as e:
        logger.error(f"❌ Error during table recreation: {e}")
        return False

if __name__ == "__main__":
    import sys
    
    print("\n" + "=" * 80)
    print("PricePulse Database Migration Tool")
    print("=" * 80)
    print("\nOptions:")
    print("1. Auto-migrate (add missing columns/tables)")
    print("2. Full recreation (DELETE ALL DATA and recreate)")
    print("3. Exit")
    
    choice = input("\nSelect option (1-3): ").strip()
    
    if choice == "1":
        success = migrate_schema()
        sys.exit(0 if success else 1)
    
    elif choice == "2":
        success = recreate_all_tables()
        sys.exit(0 if success else 1)
    
    elif choice == "3":
        print("Exiting...")
        sys.exit(0)
    
    else:
        print("Invalid choice")
        sys.exit(1)

import pandas as pd
from app.utils.logger import logger

# ========== SCHEMA VALIDATION ==========
REQUIRED_COLUMNS = ["title", "price", "availability", "rating"]

logger.info("Loading raw data...")
df = pd.read_csv("app/scraper/raw_data.csv")

# Validate schema
logger.info("Validating data schema...")
missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
if missing_columns:
    logger.error(f"Missing required columns: {missing_columns}")
    raise ValueError(f"Schema validation failed: Missing columns {missing_columns}")

logger.info("✓ Schema validation passed")

# ========== DATA QUALITY METRICS ==========
initial_rows = len(df)
initial_missing_values = df.isnull().sum().sum()
logger.info(f"Initial state: {initial_rows} rows, {initial_missing_values} missing values")

# Remove duplicates
initial_duplicates = df.duplicated().sum()
df.drop_duplicates(inplace=True)
duplicates_removed = initial_duplicates
logger.info(f"Duplicates removed: {duplicates_removed}")

# Clean price column
df["price"] = df["price"].str.replace("£", "", regex=False)
df["price"] = df["price"].astype(float)

# Standardize availability
df["availability"] = df["availability"].str.strip()

# Track missing values before filling
missing_before = df.isnull().sum().sum()
df.fillna("Unknown", inplace=True)
missing_after = df.isnull().sum().sum()
missing_filled = missing_before - missing_after
logger.info(f"Missing values filled: {missing_filled}")

# Convert ratings to numbers
rating_map = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

df["rating"] = df["rating"].map(rating_map)

# ========== DATA QUALITY SUMMARY ==========
final_rows = len(df)
rows_removed = initial_rows - final_rows

summary = {
    "rows_scraped": initial_rows,
    "duplicates_removed": duplicates_removed,
    "rows_removed": rows_removed,
    "final_rows": final_rows,
    "missing_values_filled": missing_filled,
    "quality_score": f"{(final_rows / initial_rows * 100):.2f}%"
}

logger.info("\n=== DATA QUALITY METRICS ===")
for key, value in summary.items():
    logger.info(f"{key}: {value}")
logger.info("============================\n")

# ========== SAVE CLEANED DATA ==========
# Save as CSV
df.to_csv("app/cleaning/cleaned_data.csv", index=False)
logger.info("✓ Cleaned data saved as CSV: app/cleaning/cleaned_data.csv")

# Save as JSON
df.to_json("app/cleaning/cleaned_data.json", orient="records", indent=2)
logger.info("✓ Cleaned data saved as JSON: app/cleaning/cleaned_data.json")

logger.info("Data cleaning completed successfully!")
import pandas as pd

df = pd.read_csv("app/scraper/raw_data.csv")

# Remove duplicates
df.drop_duplicates(inplace=True)

# Clean price column
df["price"] = df["price"].str.replace("£", "", regex=False)
df["price"] = df["price"].astype(float)

# Standardize availability
df["availability"] = df["availability"].str.strip()

# Fill missing values
df.fillna("Unknown", inplace=True)

# Convert ratings to numbers
rating_map = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

df["rating"] = df["rating"].map(rating_map)

# Save cleaned data
df.to_csv("app/cleaning/cleaned_data.csv", index=False)

print("Data cleaning completed!")
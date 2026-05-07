from playwright.sync_api import sync_playwright
import pandas as pd
from datetime import datetime
from app.utils.logger import logger

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
MAX_RETRIES = 3

all_books = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(user_agent=USER_AGENT)
    page = context.new_page()

    logger.info("Starting web scraping...")

    for page_num in range(1, 6):  # scrape first 5 pages
        url = BASE_URL.format(page_num)
        
        # Retry logic
        for attempt in range(MAX_RETRIES):
            try:
                logger.info(f"Scraping page {page_num} (attempt {attempt + 1}/{MAX_RETRIES})")
                page.goto(url, timeout=60000)
                break
            except Exception as e:
                logger.warning(f"Error loading page {page_num}, attempt {attempt + 1}: {e}")
                if attempt == MAX_RETRIES - 1:
                    logger.error(f"Failed to load page {page_num} after {MAX_RETRIES} attempts")
                    continue

        try:
            books = page.query_selector_all(".product_pod")
            logger.info(f"Found {len(books)} products on page {page_num}")

            for book in books:
                try:
                    title = book.query_selector("h3 a").get_attribute("title")
                    price = book.query_selector(".price_color").inner_text()
                    availability = book.query_selector(".availability").inner_text().strip()
                    rating = book.query_selector("p.star-rating").get_attribute("class").split()[-1]

                    all_books.append({
                        "title": title,
                        "price": price,
                        "availability": availability,
                        "rating": rating,
                        "scraped_at": datetime.now()
                    })

                except Exception as e:
                    logger.error(f"Error extracting book data: {e}")

        except Exception as e:
            logger.error(f"Error processing page {page_num}: {e}")

    browser.close()
    logger.info(f"Scraping completed! Total products scraped: {len(all_books)}")

df = pd.DataFrame(all_books)
df.to_csv("app/scraper/raw_data.csv", index=False)

logger.info("Data saved to app/scraper/raw_data.csv")
from playwright.sync_api import sync_playwright
import pandas as pd

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"

all_books = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    for page_num in range(1, 6):  # scrape first 5 pages
        url = BASE_URL.format(page_num)

        try:
            page.goto(url, timeout=60000)

            books = page.query_selector_all(".product_pod")

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
                        "rating": rating
                    })

                except Exception as e:
                    print("Error extracting book:", e)

        except Exception as e:
            print("Error loading page:", e)

    browser.close()

df = pd.DataFrame(all_books)

df.to_csv("app/scraper/raw_data.csv", index=False)

print("Scraping completed!")
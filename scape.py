import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
def scrape_page(url):
    headers = {
        "User-Agent": random.choice([
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"
        ])
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors

        soup = BeautifulSoup(response.content, 'html.parser')
        products = []
        product_divs = soup.find_all('div',
                                     class_="sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20")

        if not product_divs:
            print("No product divs found.")

        for product in product_divs:
            product_data = {}


            img_tag = product.find('img', class_='s-image')
            if img_tag:
                product_data['image'] = img_tag['src']
            else:
                product_data['image'] = 'N/A'


            title_span = product.find('span', class_='a-size-base-plus a-color-base a-text-normal')
            if title_span:
                product_data['title'] = title_span.text.strip()
            else:
                product_data['title'] = 'N/A'


            price_span = product.find('span', class_='a-price-whole')
            if price_span:
                product_data['price'] = price_span.text.strip()
            else:
                product_data['price'] = 'N/A'




            products.append(product_data)

        return products
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except requests.exceptions.RequestException as err:
        print(f"Error occurred: {err}")

    return []



url = 'https://www.amazon.in/s?k=kurthis&ref=nb_sb_noss'

all_products = []


for page in range(1, 17):
    page_url = f"{url}&page={page}"
    print(f"Scraping {page_url}")
    page_products = scrape_page(page_url)
    all_products.extend(page_products)



df = pd.DataFrame(all_products)


if df.empty:
    print("No data was scraped.")
else:

    df.to_excel('products.xlsx', index=False)
    print("Data scraped and saved to products.xlsx")

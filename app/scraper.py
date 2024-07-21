import requests
from bs4 import BeautifulSoup
from time import sleep
import os
from app.database import Database
from app.notifier import Notifier
from app.cache import Cache
from app.models import ScrapeSettings
from app.utils import clean_price
import logging
from dotenv import load_dotenv
import re

# Load environment variables from .env file
load_dotenv()

class Scraper:
    def __init__(self, settings: ScrapeSettings):
        self.pages_limit = settings.pages_limit
        self.proxy = settings.proxy
        self.products = []
        self.base_url = os.getenv("BASE_URL")
        self.db = Database()
        self.cache = Cache()
        self.notifier = Notifier()
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def sanitize_filename(self, title):
        # Remove invalid characters and limit the length of the filename
        sanitized_title = re.sub(r'[<>:"/\\|?*]', '', title)
        sanitized_title = sanitized_title[:255]
        return sanitized_title.strip()

    def scrape(self):
        page = 1
        while True:
            if self.pages_limit and page > self.pages_limit:
                break
            url = f"{self.base_url}?page={page}"
            try:
                response = self.fetch_page(url)
                soup = BeautifulSoup(response.text, 'html.parser')
                self.parse_products(soup)
            except Exception as e:
                self.logger.error(f"Failed to scrape {url}: {e}")
                sleep(5)  # Retry after 5 seconds
                continue
            page += 1
        self.save_to_db()
        self.notify({"products_scraped": len(self.products)})
        return {"products_scraped": len(self.products)}

    def fetch_page(self, url):
        proxies = {"http": self.proxy, "https": self.proxy} if self.proxy else None
        response = requests.get(url, proxies=proxies)
        response.raise_for_status()
        return response

    def parse_products(self, soup):
        product_cards = soup.find_all('li', class_='product')
        self.logger.info(f"Found {len(product_cards)} product cards.")
        for card in product_cards:
            try:
                title_tag = card.find('h2', class_='woo-loop-product__title').a
                price_tag = card.find('span', class_='woocommerce-Price-amount amount')
                image_tag = card.find('img', class_='attachment-woocommerce_thumbnail')

                if not title_tag or not price_tag or not image_tag:
                    self.logger.warning("Skipping a product card due to missing elements.")
                    continue

                title = title_tag.text.strip()
                price_str = price_tag.bdi.text.strip()
                price = clean_price(price_str)
                image_url = image_tag.get('data-lazy-src') or image_tag.get('src')
                if image_url.startswith('data:image/'):
                    # Skip if image URL is a placeholder
                    self.logger.warning(f"Skipping image with placeholder URL: {image_url}")
                    continue
                image_path = self.download_image(image_url, self.sanitize_filename(title))
                product = {
                    "product_title": title,
                    "product_price": price,
                    "path_to_image": image_path,
                }
                if not self.is_cached(product):
                    self.products.append(product)
                    self.cache.set(title, product)
            except Exception as e:
                self.logger.error(f"Error parsing product card: {e}")

    def download_image(self, url, title):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Ensure we got a successful response
            image_path = f'images/{title}.jpg'
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            with open(image_path, 'wb') as f:
                f.write(response.content)
            return image_path
        except Exception as e:
            self.logger.error(f"Failed to download image {url}: {e}")
            return None

    def is_cached(self, product):
        cached_product = self.cache.get(product["product_title"])
        return cached_product and cached_product["product_price"] == product["product_price"]

    def save_to_db(self):
        self.db.save(self.products)

    def notify(self, result):
        self.notifier.notify(result)

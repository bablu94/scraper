import unittest
from app.scraper import Scraper
from app.models import ScrapeSettings

class TestScraper(unittest.TestCase):
    def test_scrape(self):
        settings = ScrapeSettings(pages_limit=1)
        scraper = Scraper(settings)
        result = scraper.scrape()
        self.assertTrue("products_scraped" in result)
        self.assertIsInstance(result["products_scraped"], int)

if __name__ == "__main__":
    unittest.main()

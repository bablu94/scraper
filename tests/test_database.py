import unittest
import json
from app.database import Database

class TestDatabase(unittest.TestCase):
    def test_save(self):
        db = Database('test_products.json')
        data = [{"product_title": "Test", "product_price": 10, "path_to_image": "path/to/image.jpg"}]
        db.save(data)
        with open('test_products.json', 'r') as f:
            loaded_data = json.load(f)
        self.assertEqual(data, loaded_data)

if __name__ == "__main__":
    unittest.main()

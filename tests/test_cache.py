import unittest
from app.cache import Cache

class TestCache(unittest.TestCase):
    def test_cache(self):
        cache = Cache(ttl=5)
        cache.set("test_key", "test_value")
        self.assertEqual(cache.get("test_key"), "test_value")

if __name__ == "__main__":
    unittest.main()

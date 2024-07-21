import unittest
from app.notifier import Notifier
import sys
from io import StringIO

class TestNotifier(unittest.TestCase):
    def test_notify(self):
        notifier = Notifier()
        result = {"products_scraped": 10}
        captured_output = StringIO()
        sys.stdout = captured_output
        notifier.notify(result)
        sys.stdout = sys.__stdout__
        self.assertIn("Scraped 10 products.", captured_output.getvalue())

if __name__ == "__main__":
    unittest.main()

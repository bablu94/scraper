class Notifier:
    def notify(self, result):
        print(f"Scraped {result['products_scraped']} products.")

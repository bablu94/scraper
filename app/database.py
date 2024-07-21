import json

class Database:
    def __init__(self, filename='products.json'):
        self.filename = filename

    def save(self, data):
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=4)

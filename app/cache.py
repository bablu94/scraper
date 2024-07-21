from cachetools import TTLCache

class Cache:
    def __init__(self, ttl=300):
        self.cache = TTLCache(maxsize=1000, ttl=ttl)

    def get(self, key):
        return self.cache.get(key)

    def set(self, key, value):
        self.cache[key] = value

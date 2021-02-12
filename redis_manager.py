import os
import json
import redis


class RedisManager:
    def __init__(self, ip, port):
        self.redis_client = redis.from_url(os.getenv('REDISTOGO_URL', '127.0.0.1:6379'))

    def exists(self, key):
        return self.redis_client.exists(key)

    def get(self, key):
        return self.redis_client.get(key).decode()

    def set(self, key, value, to_json=False):
        if to_json:
            value = json.dumps(value, ensure_ascii=True)
        return self.redis_client.set(key, value)

import json
import redis


class RedisManager:
    def __init__(self, ip, port):
        self.redis_client = redis.Redis(host='redis', port=6379)

    def exists(self, key):
        return self.redis_client.exists(key)

    def get(self, key):
        return self.redis_client.get(key).decode()

    def set(self, key, value, to_json=False):
        if to_json:
            value = json.dumps(value, ensure_ascii=True)
        return self.redis_client.set(key, value)

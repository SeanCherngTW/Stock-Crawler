import json
import redis
from config import redis_to_go_ip, redis_to_go_port


class RedisManager:
    def __init__(self, ip, port):
        self.redis_client = redis.Redis(host=redis_to_go_ip, port=redis_to_go_port)

    def exists(self, key):
        return self.redis_client.exists(key)

    def get(self, key):
        return self.redis_client.get(key).decode()

    def set(self, key, value, to_json=False):
        if to_json:
            value = json.dumps(value, ensure_ascii=True)
        return self.redis_client.set(key, value)

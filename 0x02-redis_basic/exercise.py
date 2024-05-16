#!/usr/bin/env python3
"""
Main file
"""
import redis
import uuid


class Cache:
    """
    Cache class to store data in Redis
    """

    def __init__(self):
        """Initialize the Cache class with Redis client"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the input data in Redis using a random key and return the key
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key


if __name__ == "__main__":
    cache = Cache()
    data = b"hello"
    key = cache.store(data)
    print(key)
    local_redis = redis.Redis()
    print(local_redis.get(key))

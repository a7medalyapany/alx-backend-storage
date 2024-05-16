#!/usr/bin/env python3
"""
Module for Exercise.
"""
import redis
import uuid
from typing import Union, Optional, Callable


class Cache:
    """
    Cache class. Implements caching functions with a Redis client.
    """

    def __init__(self):
        """
        Initialize the Cache class.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the input data in Redis using a random key.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """
        Get the value of a string key from the Redis server.
        """
        result = self._redis.get(key)
        if fn:
            result = fn(result)
        return result

    def get_str(self, key: str) -> str:
        """
        Get the value of a string key from the Redis server and convert it to a string.
        """
        result = self.get(key, fn=str)
        return result

    def get_int(self, key: str) -> int:
        """
        Get the value of a string key from the Redis server and convert it to an integer.
        """
        result = self.get(key, fn=int)
        return result

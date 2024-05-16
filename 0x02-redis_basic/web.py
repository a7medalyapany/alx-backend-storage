#!/usr/bin/env python3
"""
Module for web.
"""
import redis
import requests
from typing import Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count how many times methods of the Cache class are called.
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function for the decorator.
        """
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


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

    @count_calls
    def get_page(self, url: str) -> str:
        """
        Get the HTML content of a particular URL and return it.
        """
        response = requests.get(url)
        key = f"count:{url}"
        self._redis.set(key, response.text, ex=10)
        return response.text

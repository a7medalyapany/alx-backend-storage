#!/usr/bin/env python3
"""
Module for Exercise.
"""
import redis
import uuid
from typing import Union, Optional, Callable
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


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs for a particular function.
    """
    inputs = f"{method.__qualname__}:inputs"
    outputs = f"{method.__qualname__}:outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function for the decorator.
        """
        self._redis.rpush(inputs, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(outputs, str(result))
        return result

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

    @call_history
    @count_calls
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


def replay(method: Callable):
    """
    Function to display the history of calls of a particular function.
    """
    inputs = method.__self__._redis.lrange(
        f"{method.__qualname__}:inputs", 0, -1)
    outputs = method.__self__._redis.lrange(
        f"{method.__qualname__}:outputs", 0, -1)
    print(f"{method.__qualname__} was called {len(inputs)} times:")
    for inp, out in zip(inputs, outputs):
        print(f"{method.__qualname__}{inp.decode('utf-8')} -> {out.decode('utf-8')}")

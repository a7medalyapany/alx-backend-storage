#!/usr/bin/env python3
''' Main module for the Task'''
import uuid
import redis


class Cache:
    '''
    Cache class to store data in Redis
    '''

    def __init__(self, host='localhost', port='5332', db=0) -> None:
        '''Initialize the Cache class with Redis client'''
        self._redis = redis.Redis(host=host, port=port, db=db)
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''
        Store the input data in Redis using a random key and return the key
        '''
        data_key = str(uuid.uuid4())
        self._redis.set(data_key, data)
        return data_key

    def get(
            self,
            key: str,
            fn: Callable = None,
    ) -> Union[str, bytes, int, float]:
        '''Gets a value
        '''
        data = self._redis.get(key)
        return fn(data) if fn is not None else data

    def get_str(self, key: str) -> str:
        '''Gets a string
        '''
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        '''Gets an integer
        '''
        return self.get(key, lambda x: int(x))

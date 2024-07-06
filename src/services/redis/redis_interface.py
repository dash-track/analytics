
from abc import ABC, abstractmethod

class RedisInterface(ABC):
    @abstractmethod
    def save(self):
        """
        Used to save data to redis, should be implemented by child class.
        Method requires a key and a hashed object value to be passed in. Creating
        the hashed value is the responsibility of the child class.
        """
        raise NotImplementedError("Method not implemented")
    
    @abstractmethod
    def load(self, key):
        """
        Used to load data from redis, should be implemented by child class.
        Method requires a key to be passed in. The key is used to retrieve the
        hashed object value from redis.

        @param key: The key to be used to retrieve the hashed value from redis
        """
        raise NotImplementedError("Method not implemented")
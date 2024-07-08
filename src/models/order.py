import sys
import pathlib
import uuid
import redis

from datetime import date

sys.path.append(f"{pathlib.Path(__file__).parent.resolve()}/../..")

from src.services.redis.redis_object import RedisObject


class Order(RedisObject):
    """
    Class representing an order. Stores all the required information about an order.
    Contains methods to save and load order data from Redis. In addition to that, also
    contains methods to manipulate order data.
    """

    def __init__(
        self,
        restaurant_name: str,
        amount_spent_total: int,
        date_of_order: date,
        order_id: uuid.UUID = None,
        items: dict = {},
        redis_client: redis.StrictRedis = None,
    ):
        """
        Initialize Order object with restaurant name, amount spent, date of order, and items.

        @param restaurant_name: Name of the restaurant
        @param amount_spent_total: Total amount spent on the order
        @param date_of_order: Date of the order
        @param items: Dictionary containing the items ordered
        @param redis_client: Redis client to be injected into the Order object
        """
        if redis_client is not None:
            assert isinstance(
                redis_client, redis.StrictRedis
            ), "Redis client passed is not an instance of redis.StrictRedis"

        self._redis_client = redis_client
        self._order_id = str(uuid.uuid4()) if order_id is None else order_id
        self._restaurant_name = restaurant_name
        self._amount_spent_total = amount_spent_total
        self._date_of_order = date_of_order
        self._items = items if items is not None else {}

    @property
    def order_id(self):
        return self._order_id

    @property
    def restaurant_name(self):
        return self._restaurant_name

    @property
    def amount_spent_total(self):
        return self._amount_spent_total

    @property
    def date_of_order(self):
        return self._date_of_order

    @property
    def items(self):
        return self._items

    def inject_redis_client(
        self, redis_client: redis.StrictRedis, override: bool = False
    ):
        """
        Inject Redis client into Order object. Required by the save and load
        methods in the RedisInterface class.

        @param redis_client: Redis client to be injected into the Order object
        """
        assert redis_client is None or override, "Redis client already injected"
        self._redis_client = redis_client

    def save(self):
        """
        Save the order data to Redis. This function takes every field present in the
        Order object and saves it as a value to the key of the order_id.

        NOTE: (Kurt, 2024-07-06) We won't check for the items field for now since we don't
        scrape the order items at this point in time. This field is expected to be empty in
        redix for the time being.
        """
        assert self._redis_client is not None and isinstance(
            self._redis_client, redis.StrictRedis
        ), "Redis client not injected"
        key_string = f"order:{self.order_id}"
        value_hash_string = {
            "restaurant_name": self._restaurant_name,
            "amount_spent_total": self._amount_spent_total,
            "date_of_order": self._date_of_order,
        }
        self._redis_client.hmset(key_string, value_hash_string)
        # assert self.items is not None, "Items field is empty"
        # ^ remove this line once we start scraping the order items
        partial_item_target_key = f"order:{self._order_id}:items:"
        for item_key, item_value in self._items.items():
            item_key = f"{partial_item_target_key}{item_key}"
            self._redis_client.hmset(item_key, item_value)

    @staticmethod
    def load(key: uuid.UUID, redis_client: redis.StrictRedis):
        """
        Get the order data from Redis. This function retrieves the order data as a
        hash from the key provided. We then extract the fields from the hash and populate
        the Order object instance with the data and return the Order object.

        @param key: The key to be used to retrieve the order data from Redis
        @param redis_client: The Redis client to be used to interact with Redis
        @return: Order object with the data retrieved from Redis
        """
        assert isinstance(
            redis_client, redis.StrictRedis
        ), "Redis client not passed to load method"
        order_details = redis_client.hgetall(f"order:{key}")
        # order_details = {
        #     k.decode("utf-8"): v.decode("utf-8") for k, v in order_details.items()
        # }

        # Get the items and quantities
        items_keys = redis_client.keys(f"order:{key}:items:*")
        items = {}
        for item_key in items_keys:
            # item_key = item_key.decode("utf-8")
            item_details = redis_client.hgetall(item_key)
            # item_details = {
            #     k.decode("utf-8"): v.decode("utf-8") for k, v in item_details.items()
            # }
            items[item_key.split(":")[-1]] = item_details

        return Order(
            order_id=key,
            restaurant_name=order_details["restaurant_name"],
            amount_spent_total=order_details["amount_spent_total"],
            date_of_order=order_details["date_of_order"],
            items=items,
            redis_client=redis_client,
        )

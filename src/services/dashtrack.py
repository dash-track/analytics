import constants
import os
import sys
import pathlib
import threading

from typing import Any

# Added to make consistent import paths with respect to src
sys.path.append(f"{pathlib.Path(__file__).parent.resolve()}/../..")

from src.services.redis.service import RedisService
from src.utils.errors import ServiceAlreadyRunningError
from src.utils.threader import LoggingPool
from src.utils.logger import LoggerBuilder


class DashTrackService:
    """
    Primary service for DashTrack. Entry point for all DashTrack processes.
    Responsible for setting up all dependency services and error handling.
    """

    def __init__(self):
        self.thread_local = None
        self.logger_builder = None
        self.redis_service = None
        self._setup()
        self._start_redis()

    def __getattribute__(self, __name: str) -> Any:
        if __name != "thread_local":
            return super().__getattribute__(__name)

    def __del__(self) -> None:
        """
        Responsible for cleaning up all resources used by the DashTrack service.
        Gracefully shuts down all services and threads.
        """
        self._teardown()

    def _setup(self) -> None:
        """
        Setup service instance on new thread, and create logger. This
        method is responsible for initializing all the builders that
        will be passed to other services.
        """
        self.thread_local = threading.local()
        self.logger_builder = LoggerBuilder()

    def _start_redis(self) -> None:
        """
        Start the Redis service.
        """
        print("Starting Redis service...", end=" ")
        self.redis_service = RedisService(
            password=f"{os.getenv('REDIS_DT_PWD', constants.REDIS_TEST_PWD)}"
        )
        try:
            self.redis_service.init()
        except ServiceAlreadyRunningError as e:
            print(e)
        assert self.redis_service.status(), "Redis service not running"
        print(f"{constants.OKGREEN}OK{constants.ENDC}")

    def _teardown(self):
        """
        Gracefully shuts down the redis client and the docker client.
        """
        # Stop Redis service
        print("Stopping Redis service...", end=" ")
        self.redis_service.stop()
        print(f"{constants.OKGREEN}OK{constants.ENDC}")
        # Delete thread local
        del self.thread_local

    def run(self) -> None:
        """
        Main entry point for the DashTrack service.
        """
        # sleep for 10 seconds
        print("Sleeping for 10 seconds...")
        import time

        time.sleep(10)
        print("Done sleeping")

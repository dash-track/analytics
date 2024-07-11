import os, pathlib
import sys

# Added to make consistent import paths with respect to src
sys.path.append(f"{pathlib.Path(__file__).parent.resolve()}/../..")
from src.services.selenium.platforms import Platform
import constants
from utils.errors import *

class Vault:
    def __init__(self):
        pass

    def configure(self):
        pass

    def unlock(self):
        pass

    def loadIntoMemory(self):
        pass

    @staticmethod
    def isAuthenticated(platform: Platform, headed_support: bool = True) -> bool:
        """
        Check if user has saved auth state for platform
        """
        if platform.login_url == "":
            return True
        platform_dir_path = pathlib.Path(
            constants.CHROME_DRIVER_COOKIE_DIR.replace(
                "<platform>", platform.name.lower()
            )
        )
        if not platform_dir_path.exists():
            if not headed_support:
                platform.non_headed_auth_instruction()
                raise NoHeadedSupportError(platform.name)
            return False
        return True
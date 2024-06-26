import pathlib
import os

#### Project Root ####
PROJECT_ROOT = f"{pathlib.Path(__file__).parent.resolve()}"

# ##### Select Menu Constants #####
# AUTO = "Automatically generate entry from url (beta)"
# ADD = "Add new job application"
# EDIT = "Edit existing job application"
# VIEW = "View all job applications"
# QUIT = "Quit"
# BKP = "Start Backup Daemon"
# PRT = "Print to file"

# CHOICE_MAP = {
#     "Automatically generate entry from url (beta)": "auto",
#     "Add new job application": "add",
#     "Edit existing job application": "edit",
#     "View all job applications": "view",
#     "Quit": "quit",
#     "Start Backup Daemon": "bkp",
#     "Print to file": "print",
# }

# ##### File Constants #####
# SOURCE_CSV = f"{PROJECT_ROOT}/job_applications.csv"
# COLUMN_NAMES = ["Company", "Position", "Date Applied", "Status", "Portal Link", "Notes"]

##### COLORS #####
OKGREEN = "\033[1;32m"
INFOBLUE = "\033[1;34m"
WARNING = "\033[1;33m"
FAIL = "\033[1;31m"
ENDC = "\033[0m"

# BAT = "./bin/bat/bat"
BAT = "bat"

YN = ["YES", "NO"]
NY = ["NO", "YES"]


#### Redis Constants ####
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_CONTAINER_NAME = "redis-trapp"
REDIS_DATA_DIR = f"{REDIS_CONTAINER_NAME}-data"
REDIS_DOCKER_IMAGE_TAG = "redis:7.2.2-bookworm"
REDIS_USERNAME = "default"
REDIS_TEST_PWD = "test"
REDIS_CHARSET = "utf-8"
REDIS_ERRORS = "strict"
REDIS_LOG_FILE = f"{PROJECT_ROOT}/logs/redis.log"
REDIS_STATUS_TMP = f"{PROJECT_ROOT}/logs/redis_status.tmp"

#### Chrome Driver Constants ####
CHROME_DRIVER_VERSIONS_JSON = "https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json"
CHROME_DRIVER_VERSIONS_CACHE = f"{PROJECT_ROOT}/.cache/chrome_driver_versions.json"

CHROME_DRIVER_SYSTEM_ARCH_MAP = {
    "Darwin arm64": "mac-arm64",
    "Darwin x86_64": "mac-x64",
    "Linux x86_64": "linux64",
}

CHROME_DRIVER_EXECUTABLE = f"{PROJECT_ROOT}/bin/chrome-driver/chromedriver-{CHROME_DRIVER_SYSTEM_ARCH_MAP[f'{os.uname().sysname} {os.uname().machine}']}/chromedriver"

CHROME_DRIVER_DEFAULT_OPTS = ["--headless"]
CHROME_DRIVER_NO_HEADLESS_OPTS = ["--no-headless"]
CHROME_DRIVER_INCOGNITO_OPTS = ["--incognito"]
CHROME_DRIVER_SERVER_OPTS = [
    "--headless",
    "--no-sandbox",
    "start-maximized",
    "disable-infobars",
    "--disable-extensions",
]
CHROME_DRIVER_COOKIE_DIR = f"{PROJECT_ROOT}/.cache/chrome_driver_<platform>"

#### Selenium Constants ####
SELENIUM_TIMEOUT = 5

#### Multiprocessing Constants ####
MAX_WORKERS = 10

#### Logging Constants ####
LOG_FILENAME = f"{PROJECT_ROOT}/logs/trapp.log"
LOG_THREADED_FILENAME = f"{PROJECT_ROOT}/logs/trapp-threaded.log"
LOG_TMP_FILENAME = f"{PROJECT_ROOT}/logs/run_error.log"
LOG_FILEMODE = "a"
LOG_FORMAT = "%(asctime)s %(name)s %(levelname)s %(message)s"
LOG_DATEFMT = "%Y-%m-%d %H:%M:%S"

#### xvfb Constants ####
XVFB_CACHE_FLAG = f"{PROJECT_ROOT}/.cache/xvfb"

#### Formula configuration ####
FORMULA_CONFIG_PATH = f"{PROJECT_ROOT}/infra/build/config/formula.json"
FORMULA_PATH = f"{PROJECT_ROOT}/infra/build/formula/out"

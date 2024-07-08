from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import sys
import pathlib
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


# Set up Chrome options
options = Options()
# options.add_argument('--headless')  # Runs Chrome in headless mode.
options.add_argument("--no-sandbox")  # Bypass OS security model
# options.add_argument('--disable-gpu')  # applicable to windows os only
options.add_argument("start-maximized")  # start maximized
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")

# Make constants accessible to services
sys.path.append(f"{pathlib.Path(__file__).parent.resolve()}/../../..")

import constants

# from bs4 import BeautifulSoup

service = Service(executable_path=constants.CHROME_DRIVER_EXECUTABLE)

driver = webdriver.Chrome(service=service, options=options)

driver.get("https://www.doordash.com/")

try:
    wait = WebDriverWait(driver, constants.SELENIUM_GLOBAL_DRIVER_WAIT_TIME)
    login_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//span[contains(@class, 'Text-sc-16fu6d-0')]")
        )
    )
    login_button.click()

except Exception as e:
    print("Error: ", e)

driver.quit()

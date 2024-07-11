from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc
import sys
import pathlib
import pickle
import os
import time
from datetime import datetime, date

sys.path.append(str(pathlib.Path(__file__).resolve().parents[4]))
import constants

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
from platforms import Platform

# Set up Chrome options
options = Options()
# options.add_argument('--headless')  # Runs Chrome in headless mode.
options.add_argument('--no-sandbox')  # Bypass OS security model
# options.add_argument('--disable-gpu')  # applicable to windows os only
options.add_argument('start-maximized')  # start maximized
# options.add_argument('disable-infobars')
# options.add_argument('--disable-extensions')

class DoorDash(Platform):
    def __init__(self, service, cookies_path):
        super().__init__(service, cookies_path)
        self.driver = self.init_undetected_driver()
    
    def init_undetected_driver(self):
        driver = uc.Chrome(service=self.service, options=options)
        return driver
    
    def quit_driver(self):
        return super().quit_driver()

    def login(self):
        self.driver.get("https://www.doordash.com/")

        try:
            wait = WebDriverWait(self.driver, constants.SELENIUM_GLOBAL_DRIVER_WAIT_TIME)
            login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'Text-sc-16fu6d-0')]")))
            login_button.click()
                
            print("Please log in to your Doordash account now.")
            time.sleep(50)
            
            cookies = self.driver.get_cookies()

            self.save_cookies(cookies)

        except Exception as e:
            print("Error: ", e)

    def save_cookies(self, cookies):
        cookie_objs = []
        for cookie in cookies:
            if cookie["domain"] == ".doordash.com":
                cookie_objs.append(
                    {
                        "name": cookie["name"],
                        "value": cookie["value"],
                        "domain": cookie["domain"],
                    }
                )
        try:
            with open(self.cookies_path, "wb") as file:
                pickle.dump(cookie_objs, file)
        except Exception as e:
            print("Error saving cookies to file: ", e)
            
    def load_cookies(self):
        try:
            with open(self.cookies_path, "rb") as file:
                cookies = pickle.load(file)
                for cookie in cookies:
                    self.driver.add_cookie(cookie)
        except Exception as e:
            print("Error loading cookies from file: ", e)

    def access_with_cookies(self):
        self.driver.get("https://www.doordash.com/orders/")

        try:
            self.load_cookies()
            self.driver.refresh()
            time.sleep(5)

        except Exception as e:
            print("Error: ", e)

# Main for testing
# class Main():
#     def __init__(self):
#         self.service = Service(executable_path=constants.CHROME_DRIVER_EXECUTABLE)
#         self.cookies_path = os.path.join(pathlib.Path(__file__).parent.resolve(), "cookies.pkl")
#         self.DD = DoorDash(self.service, self.cookies_path)

#         if not os.path.exists(self.cookies_path) or os.path.getsize(self.cookies_path) == 0:
#             print("No cookies found. Logging in.")
#             self.DD.login()
#         else:
#             print("Cookies found. Acceissing with cookies.")  
#             self.DD.access_with_cookies()
        
#         self.DD.quit_driver()

# if __name__ == "__main__":
#     Main()
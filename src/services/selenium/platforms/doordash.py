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

# Added to make consistent import paths with respect to src
sys.path.append(f"{pathlib.Path(__file__).parent.resolve()}/../../../..")
import constants
from src.services.selenium.platforms import Platform

# Set up Chrome options
options = Options()
# options.add_argument('--headless')  # Runs Chrome in headless mode.
options.add_argument('--no-sandbox')  # Bypass OS security model
# options.add_argument('--disable-gpu')  # applicable to windows os only
options.add_argument('start-maximized')  # start maximized
# options.add_argument('disable-infobars')
# options.add_argument('--disable-extensions')

class DoorDash(Platform):
    """
    DoorDash class inheriting from platform. Has functionality specific to DoorDash.
    """
    name = "DoorDash"
    base_url = "https://www.doordash.com/"
    order_url = "https://www.doordash.com/orders/"


    def __init__(self, service, cookies_path):
        super().__init__(service, cookies_path)
        self.driver = self.init_driver()
    
    def init_driver(self):
        driver = uc.Chrome(service=self.service, options=options)
        return driver

    def login(self):
        """
        Logging in to DoorDash. This prompts the user to login and then calls on the save cookies method.
        """
        self.driver.get(self.base_url)

        try:
            wait = WebDriverWait(self.driver, constants.SELENIUM_GLOBAL_DRIVER_WAIT_TIME)
            login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'Text-sc-16fu6d-0')]")))
            login_button.click()
                
            print("Please log in to your Doordash account now.")

            login_success = False
            start_time = time.time()

            while not login_success and (time.time() - start_time) < 300:
                try:
                    account_element = self.driver.find_element(By.XPATH, "//input[@aria-label='Store search: begin typing to search for stores available on DoorDash']")
                    login_success = True
                except:
                    time.sleep(1)
        
            if login_success:
                cookies = self.driver.get_cookies()
                self.save_cookies(cookies)
                print("Login successful, cookies saved.")
                self.quit_driver()
            else:
                print("Login timed out after 5 minutes.")
                self.quit_driver()

        except Exception as e:
            print("Error: ", e)

    def save_cookies(self, cookies):
        """
        Creating and saving cookie objects to a .pkl file
        """
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

    def access_with_cookies(self):
        """
        Loading cookies and accessing the order page using them.
        """
        self.driver.get(self.order_url)

        try:
            self.load_cookies(self.driver)
            self.driver.refresh()
            time.sleep(5)
            self.quit_driver()

        except Exception as e:
            print("Error: ", e)

"""
NOTE: (Baani, 2024-07-11)
- Initialize service using constants
- Initialize cookie path using constants
- Create an object of DoorDash class using the two
- If a cookie file that is populated not does exist at the cookie path, login
- Else, access using cookies
"""
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
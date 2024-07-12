import abc
import pickle

class Platform:
    """
    Parent platform class for all different food delivery platforms.
    """
    def __init__(self, service, cookies_path):
        self.service = service
        self.cookies_path = cookies_path

    @property
    def name(self):
        raise NotImplementedError
    
    @property
    def base_url(self):
        raise NotImplementedError
    
    @property
    def order_url(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    def init_driver(self):
        raise NotImplementedError("Subclasses must implement this method")
    
    def quit_driver(self):
        if self.driver:
            self.driver.quit()

    @abc.abstractmethod
    def login(self):
        raise NotImplementedError("Subclasses must implement this method")

    @abc.abstractmethod
    def save_cookies(self, cookies):
        raise NotImplementedError("Subclasses must implement this method")
    
    @abc.abstractmethod
    def load_cookies(self, driver):
        """
        Loading cookies from the saved file and adding them to the driver.
        """
        try:
            with open(self.cookies_path, "rb") as file:
                cookies = pickle.load(file)
                for cookie in cookies:
                    self.driver.add_cookie(cookie)
        except Exception as e:
            print("Error loading cookies from file: ", e)
    
    @abc.abstractmethod
    def access_with_cookies(self):
        raise NotImplementedError("Subclasses must implement this method")
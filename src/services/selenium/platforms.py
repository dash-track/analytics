import abc

class Platform:
    def __init__(self, service, cookies_path):
        self.service = service
        self.cookies_path = cookies_path

    @abc.abstractmethod
    def init_undetected_driver(self):
        raise NotImplementedError("Subclasses must implement this method")
    
    @abc.abstractmethod
    def init_selwire_driver(self):
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
        raise NotImplementedError("Subclasses must implement this method")
    
    @abc.abstractmethod
    def access_with_cookies(self):
        raise NotImplementedError("Subclasses must implement this method")
    
    # @abc.abstractmethod
    # def query_all_orders(self):
    #     raise NotImplementedError("Subclasses must implement this method")
    
    # @abc.abstractmethod
    # def add_order_total(self):
    #     raise NotImplementedError("Subclasses must implement this method")
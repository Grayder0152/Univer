import random

import selenium
import selenium.common.exceptions
import selenium.webdriver
import webdriver_manager.chrome

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

MAX_WAIT_TIME = 10
USER_AGENTS = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36"
)


class Parser:
    def __init__(self, base_url: str):
        self.base_url: str = base_url
        self.driver = self.chrome_driver()
        self.driver.implicitly_wait(5)

    @staticmethod
    def chrome_driver() -> selenium.webdriver.Chrome:
        """Return Chrome webdriver."""

        options = selenium.webdriver.ChromeOptions()
        # options.add_argument('--headless')
        # options.add_argument('--disable-extensions')
        # options.add_argument('--disable-blink-features=AutomationControlled')
        # options.add_argument('--no-sandbox')
        # options.add_argument('--disable-gpu')
        # options.add_experimental_option('excludeSwitches', ['enable-logging'])

        # service = Service(webdriver_manager.chrome.ChromeDriverManager(log_level=logging.CRITICAL).install())
        # service.creationflags = CREATE_NO_WINDOW
        driver = selenium.webdriver.Chrome(
            # service=service,
            options=options
        )
        driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": random.choice(USER_AGENTS)})
        return driver

    def open_page(self):
        self.driver.get(self.base_url)

    def find_element_by_id(self, id_: str):
        try:
            el = WebDriverWait(self.driver, MAX_WAIT_TIME).until(EC.visibility_of_element_located((By.ID, id_)))
        except selenium.common.exceptions.TimeoutException:
            pass
        else:
            return el

    def find_element_by_xpath(self, xpath: str):
        """
        Return the first element that matches the selector;
        :param xpath: str - Xpath to element;
        :return: The element is being returned.
        """

        try:
            el = WebDriverWait(self.driver, MAX_WAIT_TIME).until(EC.visibility_of_element_located((By.XPATH, xpath)))
        except selenium.common.exceptions.TimeoutException:
            pass
        else:
            return el

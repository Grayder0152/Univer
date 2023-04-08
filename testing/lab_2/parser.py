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
    def __init__(self):
        self.driver = self.chrome_driver()
        self.driver.implicitly_wait(5)

    @staticmethod
    def chrome_driver() -> selenium.webdriver.Chrome:
        """Return Chrome webdriver."""

        options = selenium.webdriver.ChromeOptions()
        driver = selenium.webdriver.Chrome(
            options=options
        )
        driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": random.choice(USER_AGENTS)})
        return driver

    def open_page(self, url: str):
        self.driver.get(url)

    def close(self):
        self.driver.close()

    def quit(self):
        self.driver.quit()

    def find_element_by_id(self, id_: str):
        try:
            el = WebDriverWait(self.driver, MAX_WAIT_TIME).until(EC.visibility_of_element_located((By.ID, id_)))
        except selenium.common.exceptions.TimeoutException:
            pass
        else:
            return el

    def find_element_by_xpath(self, xpath: str):
        try:
            el = WebDriverWait(self.driver, MAX_WAIT_TIME).until(EC.visibility_of_element_located((By.XPATH, xpath)))
        except selenium.common.exceptions.TimeoutException:
            pass
        else:
            return el

    def find_elements_by_class(self, class_: str):
        try:
            el = WebDriverWait(self.driver, MAX_WAIT_TIME).until(
                EC.visibility_of_all_elements_located((By.CLASS_NAME, class_)))
        except selenium.common.exceptions.TimeoutException:
            pass
        else:
            return el

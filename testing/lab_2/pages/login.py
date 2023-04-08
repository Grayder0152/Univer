from pages.base import DemoWebShopBasePage


class LoginPage(DemoWebShopBasePage):
    RELATED_PATH = 'login'

    EMAIL_ID_FIELD = 'Email'
    PASSWORD_ID_FIELD = 'Password'
    LOGIN_BTN_CLASS = 'login-button'

    def login(self, email: str, password: str):
        self.parser.open_page(self.url)
        self.parser.find_element_by_id(self.EMAIL_ID_FIELD).send_keys(email)
        self.parser.find_element_by_id(self.PASSWORD_ID_FIELD).send_keys(password)
        self.click_login_btn()

    def click_login_btn(self):
        self.parser.find_elements_by_class(self.LOGIN_BTN_CLASS)[0].click()

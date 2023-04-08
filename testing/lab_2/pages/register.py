import random
from pages.base import DemoWebShopBasePage


class RegisterPage(DemoWebShopBasePage):
    RELATED_PATH = 'register'

    GENDER_FIELD_ID = 'gender-{}'
    FIRST_NAME_FIELD_ID = 'FirstName'
    LAST_NAME_FIELD_ID = 'LastName'
    EMAI_FIELD_ID = 'Email'
    PASSWORD_FIELD_ID = 'Password'
    CONFIRM_PASSWORD_FIELD_ID = 'ConfirmPassword'
    REGISTER_BTN_FIELD_ID = 'register-button'

    def register(
            self, gender: str = 'male', name: str = 'Tester',
            last_name: str = 'Tester', email: str = f'tester_{random.randint(100000, 999999)}@gmail.com',
            password: str = '12345678', confirm_password: str = '12345678'
    ):
        self.parser.open_page(self.url)

        self.parser.find_element_by_id(self.GENDER_FIELD_ID.format(gender)).click()
        self.parser.find_element_by_id(self.FIRST_NAME_FIELD_ID).send_keys(name)
        self.parser.find_element_by_id(self.LAST_NAME_FIELD_ID).send_keys(last_name)
        self.parser.find_element_by_id(self.EMAI_FIELD_ID).send_keys(email)

        self.parser.find_element_by_id(self.PASSWORD_FIELD_ID).send_keys(password)
        self.parser.find_element_by_id(self.CONFIRM_PASSWORD_FIELD_ID).send_keys(confirm_password)
        self.click_register_btn()

    def click_register_btn(self):
        self.parser.find_element_by_id(self.REGISTER_BTN_FIELD_ID).click()

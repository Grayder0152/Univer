import random
import unittest

from pages import LoginPage, ProductPage, RegisterPage
from parser import Parser


class DemoWebShopRegisterTestCase(unittest.TestCase):
    VALIDATION_ERRORS = {
        'name': 'First name is required.',
        'last_name': 'Last name is required.',
        'email': 'Email is required.',
        'password': 'Password is required.',
        'confirm_password': 'Password is required.'
    }

    def setUp(self):
        self.parser = Parser()
        self.page = RegisterPage(self.parser)

    def test_validation_error_register(self):
        self.page.register(name='', last_name='', email='', password='', confirm_password='')
        errors_element = self.parser.find_elements_by_class('field-validation-error')
        for error in errors_element:
            self.assertIn(error.text, self.VALIDATION_ERRORS.values())

    def test_password_not_eq(self):
        self.page.register(password='12345678', confirm_password='11111111')
        error = 'The password and confirmation password do not match.'
        errors_element = self.parser.find_elements_by_class('field-validation-error')
        self.assertNotEqual(len(errors_element), 0)
        self.assertEqual(errors_element[0].text, error)

    def test_email_already_exist(self):
        email = f"email_{random.randint(10000, 99999)}@gmail.com"
        error = 'The specified email already exists'
        self.page.register(email=email)
        self.page.register(email=email)
        errors_element = self.parser.find_elements_by_class('validation-summary-errors')
        self.assertNotEqual(len(errors_element), 0)
        self.assertEqual(errors_element[0].text, error)

    def test_register(self):
        self.page.register()
        result = self.parser.find_elements_by_class('result')
        self.assertNotEqual(len(result), 0)
        self.assertEqual(result[0].text, 'Your registration completed')

    def tearDown(self):
        self.parser.close()
        self.parser.quit()


class DemoWebShopLoginTestCase(unittest.TestCase):
    LOGIN_ERROR = 'Login was unsuccessful. Please correct the errors and try again.\nNo customer account found'

    def _check_error(self):
        errors_element = self.parser.find_elements_by_class('validation-summary-errors')
        self.assertNotEqual(len(errors_element), 0)
        self.assertEqual(errors_element[0].text, self.LOGIN_ERROR)

    def setUp(self):
        self.parser = Parser()
        self.page = LoginPage(self.parser)

    def test_send_empty_form(self):
        self.page.login(email='', password='')
        self._check_error()

    def test_not_exist_user(self):
        self.page.login(email='not_exist_email@gmail.com', password='11111111')
        self._check_error()

    def test_exist_user(self):
        email = f'exist_user_{random.random()}@gmail.com'
        password = '12345678'
        RegisterPage(self.parser).register(email=email, password=password, confirm_password=password)

        self.page.login(email, password)
        account = self.parser.find_elements_by_class('account')
        self.assertNotEqual(len(account), 0)
        self.assertEqual(account[0].text, email)

        logout = self.parser.find_elements_by_class('ico-logout')
        logout[0].click()
        account = self.parser.find_elements_by_class('account')
        self.assertEqual(account[0].text, "My account")

    def tearDown(self):
        self.parser.close()
        self.parser.quit()


class DemoWebShopAddToCardTestCase(unittest.TestCase):
    PRODUCT_URL = '25-virtual-gift-card'
    SUCCESS_MSG = 'The product has been added to your shopping cart'

    VALID_ERRORS = (
        'Enter valid recipient name',
        'Enter valid recipient email',
        'Enter valid sender name',
        'Enter valid sender email'
    )

    def _check_cart_count(self, c: int):
        product_count = self.parser.find_elements_by_class('cart-qty')
        self.assertNotEqual(len(product_count), 0)
        self.assertEqual(product_count[0].text, f"({c})")

    def setUp(self):
        self.parser = Parser()
        self.page = ProductPage(self.parser, self.PRODUCT_URL)

    def test_send_empty_form(self):
        self.page.add_to_cart('', '', '', '')
        self._check_cart_count(0)
        notif_msg = self.parser.find_element_by_id('bar-notification').text
        for error in self.VALID_ERRORS:
            self.assertIn(error, notif_msg)
        self._check_cart_count(0)

    def test_add_to_cart(self):
        self.page.add_to_cart('Sergey', 'my_email@gmail.com', 'Sergey', 'my_email@gmail.com')
        self._check_cart_count(0)
        notif_msg = self.parser.find_element_by_id('bar-notification').text
        self.assertIn(self.SUCCESS_MSG, notif_msg)
        self._check_cart_count(1)

    def tearDown(self):
        self.parser.close()
        self.parser.quit()


if __name__ == "__main__":
    unittest.main()

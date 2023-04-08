from pages.base import DemoWebShopBasePage
from parser import Parser


class ProductPage(DemoWebShopBasePage):
    RELATED_PATH = ''

    RECIPIENTS_NAME_ID_FIELD = 'giftcard_2_RecipientName'
    RECIPIENTS_EMAIL_ID_FIELD = 'giftcard_2_RecipientEmail'
    SENDER_NAME_ID_FIELD = 'giftcard_2_SenderName'
    SENDER_EMAIL_ID_FIELD = 'giftcard_2_SenderEmail'

    ADD_TO_CARD_BTN_ID_FIELD = 'add-to-cart-button-2'

    def __init__(self, parser: Parser, product_url: str):
        super().__init__(parser)
        self.url = f"{self.url}{product_url}"

    def add_to_cart(self, recipients_name: str, recipients_email: str, sender_name: str, sender_email: str):
        self.parser.open_page(self.url)
        self.parser.find_element_by_id(self.RECIPIENTS_NAME_ID_FIELD).send_keys(recipients_name)
        self.parser.find_element_by_id(self.RECIPIENTS_EMAIL_ID_FIELD).send_keys(recipients_email)
        self.parser.find_element_by_id(self.SENDER_NAME_ID_FIELD).send_keys(sender_name)
        self.parser.find_element_by_id(self.SENDER_EMAIL_ID_FIELD).send_keys(sender_email)

        self.click_add_btn()

    def click_add_btn(self):
        self.parser.find_element_by_id(self.ADD_TO_CARD_BTN_ID_FIELD).click()

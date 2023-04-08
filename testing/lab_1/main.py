from parser import Parser


def test_demowebshop_incorrect_login():
    url = "http://demowebshop.tricentis.com/"
    error_message = "The credentials provided are incorrect"
    random_email = "test@mailinator.com"
    random_password = "121212312411"

    login_menu_btn = "/html/body/div[4]/div[1]/div[1]/div[2]/div[1]/ul/li[2]/a"
    loging_btn = "/html/body/div[4]/div[1]/div[4]/div[2]/div/div[2]/div[1]/div[2]/div[2]/form/div[5]/input"
    error_block = "/html/body/div[4]/div[1]/div[4]/div[2]/div/div[2]/div[1]/div[2]/div[2]/form/div[1]"

    parser = Parser(url)
    try:
        parser.open_page()
        parser.find_element_by_xpath(login_menu_btn).click()
        parser.find_element_by_id("Email").send_keys(random_email)
        parser.find_element_by_id("Password").send_keys(random_password)
        parser.find_element_by_xpath(loging_btn).click()

        error_block = parser.find_element_by_xpath(error_block)
        try:
            assert error_message in error_block.text
        except (AttributeError, AssertionError):
            raise AssertionError("Invalid logic of login.")
    finally:
        parser.driver.close()
        parser.driver.quit()


class TestPastebin:
    BASE_URL = 'https://pastebin.com/'

    def __init__(self):
        self.parser = Parser(self.BASE_URL)

    def test_create_post(self):
        any_text = "Any text"
        create_btn = "/html/body/div[1]/div[2]/div[1]/div[2]/div/form/div[5]/div[1]/div[10]/button"

        try:
            self.parser.open_page()

            self.parser.find_element_by_id("postform-text").send_keys(any_text)
            self.parser.find_element_by_id("postform-name").send_keys(any_text)

            self._select_paste_expiration_item_10_min()
            self.parser.find_element_by_xpath(create_btn).click()
            assert self.parser.find_element_by_xpath(
                "/html/body/div[1]/div[2]/div[1]/div[1]/div[2]/div[3]/div[1]/h1").text == any_text
            assert self.parser.find_element_by_xpath(
                "/html/body/div[1]/div[2]/div[1]/div[1]/div[4]/div[2]/ol/li/div").text == any_text
            assert "10 min" in self.parser.find_element_by_xpath(
                "/html/body/div[1]/div[2]/div[1]/div[1]/div[2]/div[3]/div[2]/div[5]").text.lower()
        except (AttributeError, AssertionError):
            raise AssertionError("Test failed")
        finally:
            self.parser.driver.close()
            self.parser.driver.quit()

    def _select_paste_expiration_item_10_min(self):
        self.parser.find_element_by_id("select2-postform-expiration-container").click()
        self.parser.find_element_by_xpath("/html/body/span[2]/span/span[2]/ul/li[3]").click()


if __name__ == '__main__':
    TestPastebin().test_create_post()
    test_demowebshop_incorrect_login()

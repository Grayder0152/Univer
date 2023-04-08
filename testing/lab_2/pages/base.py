from parser import Parser


class DemoWebShopBasePage:
    BASE_PATH = "https://demowebshop.tricentis.com"
    RELATED_PATH = None

    def __init__(self, parser: Parser):
        self.parser = parser
        if self.RELATED_PATH is None:
            raise ValueError('Set related path for page object.')

        self.url = f"{self.BASE_PATH}/{self.RELATED_PATH}"

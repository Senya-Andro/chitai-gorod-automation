from selenium.webdriver.common.by import By
from .base_page import BasePage

class ProductPage(BasePage):
    PRODUCT_TITLE = (By.CSS_SELECTOR, "h1.detail-product__header-title")
    BUY_BUTTON = (By.CSS_SELECTOR, ".product-offer-button.chg-app-button--brand-blue .chg-app-button__content")
    CONFIRM_BUTTON = (By.CSS_SELECTOR, ".chg-app-button--green")
    FAVORITE = (By.CSS_SELECTOR, ".product-buttons__fav")
    PRICE = (By.CSS_SELECTOR, ".product-offer-price__current")

    def get_title(self):
        return self.find_element(self.PRODUCT_TITLE).text

    def add_to_cart(self):
        self.click(self.BUY_BUTTON)

    def is_buy_button_present(self):
        return self.find_element(self.BUY_BUTTON).is_displayed()

    def is_in_cart(self):
        return self.find_element(self.CONFIRM_BUTTON).is_displayed()

    def add_to_favorite(self):
        self.click(self.FAVORITE)

    def get_price(self):
        return self.find_element(self.PRICE).text
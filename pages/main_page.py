from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from .base_page import BasePage

class MainPage(BasePage):
    SEARCH_INPUT = (By.CSS_SELECTOR, ".header-search__input")
    SEARCH_BUTTON = (By.CSS_SELECTOR, ".header-search__button")
    CATALOG_BUTTON = (By.CSS_SELECTOR, ".catalog__button")
    MENU_ITEMS = (By.CSS_SELECTOR, ".categories-menu__item")
    MENU_LINKS = (By.CSS_SELECTOR, ".categories-menu__item[href]")
    SUBMENU_ITEMS = (By.CSS_SELECTOR, ".categories-menu__item-title")
    SORT_DROPDOWN = (By.CSS_SELECTOR, ".chg-app-custom-dropdown")
    SORT_PRICE = (By.XPATH, "//div[contains(@class, 'chg-app-dropdown-custom-item') and text()='Сначала дешевые']")
    PRODUCT_CARD = (By.CSS_SELECTOR, "article.product-card")

    def open(self):
        self.driver.get("https://www.chitai-gorod.ru/")
        print("Открыта страница https://www.chitai-gorod.ru/")
        try:
            print("Ожидаем всплывающее окно выбора города...")
            accept_button = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".change-city__button--accept"))
            )
            print("Всплывающее окно найдено, кликаем на 'Принять'...")
            try:
                accept_button.click()
            except ElementClickInterceptedException:
                print("Клик перехватывается, используем JavaScript...")
                self.driver.execute_script("arguments[0].click();", accept_button)
        except TimeoutException as e:
            print(f"Всплывающее окно не появилось в течение 15 секунд: {e}")
            # Продолжаем, если окно не появилось (возможно, город уже выбран)

        # Ждем загрузки страницы и видимости поля поиска
        try:
            print("Ожидаем видимости поля поиска...")
            WebDriverWait(self.driver, 15).until(
                EC.visibility_of_element_located(self.SEARCH_INPUT)
            )
            print("Поле поиска найдено!")
        except TimeoutException as e:
            print(f"Не удалось найти поле поиска: {e}")
            raise

    def search(self, query):
        self.input_text(self.SEARCH_INPUT, query)
        self.click(self.SEARCH_BUTTON)

    def get_menu_items(self):
        self.click(self.CATALOG_BUTTON)
        return self.driver.find_elements(*self.MENU_ITEMS)

    def get_menu_links(self):
        self.click(self.CATALOG_BUTTON)
        return self.driver.find_elements(*self.MENU_LINKS)

    def get_submenu_items(self):
        return self.driver.find_elements(*self.SUBMENU_ITEMS)

    def sort_by_price(self):
        # Сначала кликаем на выпадающий список сортировки
        try:
            print("Открываем выпадающий список сортировки...")
            self.click(self.SORT_DROPDOWN)
            # Ждем, пока список раскроется
            WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".chg-app-dropdown-custom-item"))
            )
        except TimeoutException as e:
            print(f"Не удалось открыть выпадающий список сортировки: {e}")
            raise
        # Затем кликаем на пункт "Сначала дешевые"
        try:
            print("Выбираем 'Сначала дешевые'...")
            self.click(self.SORT_PRICE)
        except TimeoutException as e:
            print(f"Не удалось найти пункт 'Сначала дешевые': {e}")
            raise
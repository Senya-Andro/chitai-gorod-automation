import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from pages.main_page import MainPage
from selenium.webdriver.support.ui import WebDriverWait
from pages.product_page import ProductPage
from config.env import Config
import allure

@pytest.fixture(scope="module")
def driver():
    driver_path = ChromeDriverManager().install()
    if not driver_path.endswith("chromedriver.exe"):
        driver_path = driver_path.replace("THIRD_PARTY_NOTICES.chromedriver", "chromedriver.exe")
    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

@allure.feature("UI Tests")
class TestUI:
    @allure.title("Проверка работы главного меню")
    def test_main_menu_navigation(self, driver):
        page = MainPage(driver)
        page.open()
        try:
            menu_links = page.get_menu_links()
            assert len(menu_links) > 0, f"Ссылки в меню не найдены. Локатор: {page.MENU_LINKS}"
            # Кликаем на первую ссылку (например, "Комиксы")
            first_link = menu_links[0]
            first_link_text = first_link.find_element(By.CSS_SELECTOR, ".categories-menu__item-title").text
            first_link.click()
            WebDriverWait(driver, 5).until(
                lambda d: d.current_url != Config.BASE_URL
            )
            assert driver.current_url != Config.BASE_URL, f"Переход по '{first_link_text}' не произошел"
        except TimeoutException:
            pytest.fail("Не удалось найти ссылки в меню или выполнить переход")

    @allure.title("Проверка поиска по ключевым словам")
    def test_search_by_keyword(self, driver):
        page = MainPage(driver)
        page.open()
        try:
            page.search("Python")
            assert "Python" in driver.page_source, "Результаты поиска не содержат ключевое слово"
        except TimeoutException:
            pytest.fail("Не удалось найти поле поиска или кнопку")

    @allure.title("Проверка добавления товара в корзину")
    def test_add_to_cart(self, driver):
        main_page = MainPage(driver)
        product_page = ProductPage(driver)
        main_page.open()
        main_page.search("Книга")
        try:
            driver.find_elements(By.CSS_SELECTOR, "article.product-card")[0].click()
            product_page.add_to_cart()
            assert product_page.is_in_cart(), "Товар не добавлен в корзину"
        except TimeoutException:
            pytest.fail("Не удалось найти товар или кнопку 'Купить'")

    @allure.title("Проверка отображения информации о товаре")
    def test_product_info_display(self, driver):
        main_page = MainPage(driver)
        product_page = ProductPage(driver)
        main_page.open()
        main_page.search("Книга")
        try:
            driver.find_elements(By.CSS_SELECTOR, "article.product-card")[0].click()
            title = product_page.get_title()
            assert title, "Название товара не отображается"
        except TimeoutException:
            pytest.fail("Не удалось найти товар или название")

    @allure.title("Проверка сортировки по цене")
    def test_sort_by_price(self, driver):
        page = MainPage(driver)
        page.open()
        page.search("Книга")
        try:
            page.sort_by_price()
            prices = [float(p.text.replace(" ₽", "").replace(" ", "")) for p in
                      driver.find_elements(By.CSS_SELECTOR, ".product-offer-price__current")[:5]]
            assert all(prices[i] <= prices[i+1] for i in range(len(prices)-1)), "Сортировка по цене некорректна"
        except TimeoutException:
            pytest.fail("Не удалось найти элементы сортировки или цены")
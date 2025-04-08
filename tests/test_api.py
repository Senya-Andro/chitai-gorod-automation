# tests/test_api.py
import pytest
import requests
from config.env import Config
import allure

# Базовые заголовки для всех запросов
headers = {
    "accept": "application/json, text/plain, */*",
    "authorization": Config.BEARER_TOKEN
}

@allure.feature("API Tests")
class TestAPI:
    @allure.title("Поиск товара по части названия")
    def test_search_by_partial_name(self):
        params = {
            "customerCityId": 4,
            "phrase": "список ши",
            "products[page]": 1,
            "products[per-page]": 48,
            "sortPreset": "relevance"
        }
        with allure.step("Отправляем запрос на поиск товара по части названия"):
            response = requests.get(f"{Config.API_BASE_URL}/api/v2/search/product", headers=headers, params=params)
            assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"

        with allure.step("Проверяем структуру ответа"):
            data = response.json()
            assert "data" in data, "Ответ не содержит поле 'data'"
            assert "relationships" in data["data"], "Ответ не содержит поле 'relationships'"
            assert "products" in data["data"]["relationships"], "Ответ не содержит поле 'products' в 'relationships'"
            assert "data" in data["data"]["relationships"]["products"], "Ответ не содержит поле 'data' в 'relationships.products'"

        with allure.step("Проверяем, что список товаров не пуст"):
            products = data["data"]["relationships"]["products"]["data"]
            assert len(products) > 0, "Список товаров пуст"

    @allure.title("Поиск товара по полному названию")
    def test_search_by_full_name(self):
        params = {
            "customerCityId": 4,
            "phrase": "список шиндлера",
            "products[page]": 1,
            "products[per-page]": 48,
            "sortPreset": "relevance"
        }
        with allure.step("Отправляем запрос на поиск товара по полному названию"):
            response = requests.get(f"{Config.API_BASE_URL}/api/v2/search/product", headers=headers, params=params)
            assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"

        with allure.step("Проверяем структуру ответа"):
            data = response.json()
            assert "data" in data, "Ответ не содержит поле 'data'"
            assert "relationships" in data["data"], "Ответ не содержит поле 'relationships'"
            assert "products" in data["data"]["relationships"], "Ответ не содержит поле 'products' в 'relationships'"
            assert "data" in data["data"]["relationships"]["products"], "Ответ не содержит поле 'data' в 'relationships.products'"

        with allure.step("Проверяем, что список товаров не пуст"):
            products = data["data"]["relationships"]["products"]["data"]
            assert len(products) > 0, "Список товаров пуст"

        with allure.step("Проверяем, что книга 'Список Шиндлера' присутствует в результатах"):
            product_ids = [product["id"] for product in products]
            assert "2945480" in product_ids, "Книга 'Список Шиндлера' не найдена (ожидаемый id: 2945480)"

    @allure.title("Поиск товара с использованием фильтров")
    def test_search_with_filters(self):
        params = {
            "filters[onlyBestseller]": 1,
            "filters[authors]": 604355,
            "customerCityId": 4,
            "phrase": "гарри поттер",
            "products[page]": 1,
            "products[per-page]": 48,
            "sortPreset": "relevance"
        }
        with allure.step("Отправляем запрос на поиск товара с фильтрами"):
            response = requests.get(f"{Config.API_BASE_URL}/api/v2/search/product", headers=headers, params=params)
            assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"

        with allure.step("Проверяем структуру ответа"):
            data = response.json()
            assert "data" in data, "Ответ не содержит поле 'data'"
            assert "relationships" in data["data"], "Ответ не содержит поле 'relationships'"
            assert "products" in data["data"]["relationships"], "Ответ не содержит поле 'products' в 'relationships'"
            assert "data" in data["data"]["relationships"]["products"], "Ответ не содержит поле 'data' в 'relationships.products'"

        with allure.step("Проверяем, что список товаров не пуст"):
            products = data["data"]["relationships"]["products"]["data"]
            assert len(products) > 0, "Список товаров пуст"

    @allure.title("Поиск товара по несуществующему названию")
    def test_search_nonexistent_name(self):
        params = {
            "customerCityId": 4,
            "phrase": "несуществующий товар 12345",
            "products[page]": 1,
            "products[per-page]": 48,
            "sortPreset": "relevance"
        }
        with allure.step("Отправляем запрос на поиск товара по несуществующему названию"):
            response = requests.get(f"{Config.API_BASE_URL}/api/v2/search/product", headers=headers, params=params)
            assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"

        with allure.step("Проверяем структуру ответа"):
            data = response.json()
            assert "data" in data, "Ответ не содержит поле 'data'"
            assert "relationships" in data["data"], "Ответ не содержит поле 'relationships'"
            assert "products" in data["data"]["relationships"], "Ответ не содержит поле 'products' в 'relationships'"
            assert "data" in data["data"]["relationships"]["products"], "Ответ не содержит поле 'data' в 'relationships.products'"

        with allure.step("Проверяем, что API возвращает результаты с коррекцией"):
            products = data["data"]["relationships"]["products"]["data"]
            assert len(products) > 0, "Список товаров пуст, хотя API возвращает результаты с коррекцией"

    @allure.title("Поиск товара с пустым запросом")
    def test_search_empty_query(self):
        params = {
            "suggests[page]": 1,
            "suggests[per-page]": 5,
            "phrase": "",
            "include": "products,authors,bookCycles,publisherSeries,publishers,categories"
        }
        with allure.step("Отправляем запрос на поиск с пустой фразой"):
            response = requests.get(f"{Config.API_BASE_URL}/api/v2/search/search-phrase-suggests", headers=headers, params=params)
            assert response.status_code == 422, f"Ожидался код 422, получен {response.status_code}"

        with allure.step("Проверяем, что API возвращает ошибку"):
            data = response.json()
            assert "errors" in data, "Ответ не содержит поле 'errors'"
            assert len(data["errors"]) > 0, "Список ошибок пуст"

        with allure.step("Проверяем сообщение об ошибке"):
            assert data["errors"][0]["title"] == "Значение не должно быть пустым.", "Неверное сообщение об ошибке"

    @allure.title("Поиск товара с некорректными символами")
    def test_search_invalid_characters(self):
        params = {
            "suggests[page]": 1,
            "suggests[per-page]": 5,
            "phrase": "%%%%%",
            "include": "products,authors,bookCycles,publisherSeries,publishers,categories"
        }
        with allure.step("Отправляем запрос на поиск с некорректными символами"):
            response = requests.get(f"{Config.API_BASE_URL}/api/v2/search/search-phrase-suggests", headers=headers, params=params)
            assert response.status_code == 422, f"Ожидался код 422, получен {response.status_code}"

        with allure.step("Проверяем, что API возвращает ошибку"):
            data = response.json()
            assert "errors" in data, "Ответ не содержит поле 'errors'"
            assert len(data["errors"]) > 0, "Список ошибок пуст"

        with allure.step("Проверяем сообщение об ошибке"):
            assert data["errors"][0]["title"] == "Недопустимая поисковая фраза", "Неверное сообщение об ошибке"

    @allure.title("Поиск товара с числовым значением")
    def test_search_numeric_query(self):
        params = {
            "customerCityId": 4,
            "phrase": "516484548416846546878-54465465",
            "products[page]": 1,
            "products[per-page]": 48,
            "sortPreset": "relevance"
        }
        with allure.step("Отправляем запрос на поиск с числовым значением"):
            response = requests.get(f"{Config.API_BASE_URL}/api/v2/search/product", headers=headers, params=params)
            assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"

        with allure.step("Проверяем структуру ответа"):
            data = response.json()
            assert "data" in data, "Ответ не содержит поле 'data'"
            assert "relationships" in data["data"], "Ответ не содержит поле 'relationships'"
            assert "products" in data["data"]["relationships"], "Ответ не содержит поле 'products' в 'relationships'"
            assert "data" in data["data"]["relationships"]["products"], "Ответ не содержит поле 'data' в 'relationships.products'"

        with allure.step("Проверяем, что список товаров пуст"):
            products = data["data"]["relationships"]["products"]["data"]
            assert len(products) == 0, "Список товаров должен быть пуст"
# config/env.py
from utils.auth import get_anonymous_token


class Config:
    """
    Класс для хранения конфигурационных данных проекта.

    Attributes:
        BASE_URL (str): Базовый URL сайта Читай-город.
        API_BASE_URL (str): Базовый URL для API Читай-город.
        BEARER_TOKEN (str): Токен для авторизации в API, получаемый через get_anonymous_token.
    """
    BASE_URL = "https://www.chitai-gorod.ru/"
    API_BASE_URL = "https://web-gate.chitai-gorod.ru/"
    BEARER_TOKEN = get_anonymous_token()  # Получаем токен при импорте
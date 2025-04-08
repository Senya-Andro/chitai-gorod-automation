# utils/auth.py
import requests


def get_anonymous_token():
    """
    Получает анонимный токен для доступа к API Читай-город.

    Returns:
        str: Токен в формате "Bearer <token>", который можно использовать в заголовке Authorization.

    Raises:
        Exception: Если не удалось получить токен (например, из-за ошибки сети или неверного ответа сервера).
    """
    url = "https://web-gate.chitai-gorod.ru/api/v1/auth/anonymous"
    headers = {
        "accept": "application/json, text/plain, */*"
    }
    response = requests.post(url, headers=headers)
    if response.status_code in (200, 201):  # Принимаем 200 и 201 как успешные коды
        data = response.json()
        # Токен уже содержит префикс "Bearer", поэтому возвращаем его как есть
        return data["token"]["accessToken"]
    else:
        raise Exception(f"Не удалось получить токен: {response.status_code}, {response.text}")
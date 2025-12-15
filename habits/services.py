import requests
from django.conf import settings


def send_telegram_message(chat_id: str, text: str):
    url = f'https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/sendMessage'

    params = {
        'chat_id': chat_id,
        'text': text,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f'Ошибка отправки сообщения в Telegram: {e}')
        return False

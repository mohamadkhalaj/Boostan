import re
import urllib.parse
from pprint import pprint

import requests
from bs4 import BeautifulSoup


class Boostan:

    login_url = "https://stu.ikiu.ac.ir/foodlog.aspx"
    main_food_url = "https://stu.ikiu.ac.ir/desktopfood.aspx"
    food_list_url = "https://stu.ikiu.ac.ir/layers.aspx?quiz=resfood"
    food_reserve_url = "https://stu.ikiu.ac.ir/foodrezerv.aspx?quiz=restfood"
    forget_code_url = "https://stu.ikiu.ac.ir/layers.aspx?quiz=forgetcartfood"

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.cookie = ""
        self.name = ""
        self.credit = 0
        self.list = {}
        self.session_cookie = {}

    def login(self):
        headers = {
            "Host": "stu.ikiu.ac.ir",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:101.0) Gecko/20100101 Firefox/101.0",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "X-Requested-With": "XMLHttpRequest",
            "X-Microsoftajax": "Delta=true",
            "Cache-Control": "no-cache",
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
            "Origin": "https://stu.ikiu.ac.ir",
            "Dnt": "1",
            "Referer": "https://stu.ikiu.ac.ir/foodlog.aspx",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
        }

        data = f"ctl00%24Scm=ctl00%24UpdatePanel1%7Cctl00%24main%24bts&__EVENTTARGET=&__EVENTARGUMENT=&__VIEWSTATE=%2FwEPDwUKLTM1ODQ5NzI2NQ9kFgJmD2QWAgIDD2QWAgIDD2QWAmYPZBYMAgEPFgIeBFRleHRlZAIKDxYCHgdWaXNpYmxlaGQCDA8WAh4JaW5uZXJodG1sBSHahtmH2KfYsdi02YbYqNmHINiMIDgg2KrZitixIDE0MDFkAhIPFgIfAWhkAhQPDxYCHwFoZBYCAg0PFgIfAWhkAhYPZBYCAgEPZBYCAgEPFgIfAAWjJiA8bWFycXVlZSBvbm1vdXNlb3Zlcj0ndGhpcy5zdG9wKCknIG9ubW91c2VvdXQ9J3RoaXMuc3RhcnQoKScgc2Nyb2xsYW1vdW50PScyJyBzY3JvbGxkZWxheT0nNicgZGlyZWN0aW9uPSd1cCcgaGVpZ2h0PScyMDAnIGRpcj0ncnRsJyBzdHlsZT0ndGV4dC1hbGlnbjoganVzdGlmeTsnPiA8ZGl2IGNsYXNzPSdzbGlkZXItY29udGFpbmVyJz4gPGg0PjxhIHRhcmdldD0nX2JsYW5rJyBocmVmPSdsYXllcnMuYXNweD9xdWl6PXNob3duZXdzJmFtcDtuaWQ9MjYxICc%2B2KfYt9mE2KfYuduM2Ycg2LrYsNin24wg2LHZiNiyINmB2LHZiNi0PC9hPjwvaDQ%2BIDxwPjxwPjxzdHJvbmc%2B2KjZhyDYp9i32YTYp9i5INqp2YTbjNmHINiv2KfZhti02KzZiNuM2KfZhiDYudiy24zYsiDYs9in2qnZhiDYr9ixINiz2YTZgSDYrtmI2KfYqNqv2KfZhyDZhduMJnp3bmo72LHYs9in2YbYrzombmJzcDs8L3N0cm9uZz48L3A%2BDQoNCjxwPjxzdHJvbmc%2B2Ko8L3N0cm9uZz48c3Ryb25nPtit2YjbjNmEINi62LDYp9uMINix2YjYsiDZgdix2YjYtCDYtdix2YHYpyDYr9ixIDxzcGFuIHN0eWxlPSJjb2xvcjojRkYwMDAwOyI%2B2LPZhNmBINmH2KfbjCDYqNmH2KfYsSDZiCDYqNin2LHYp9mGIDwvc3Bhbj7YtdmI2LHYqiDZhduMINqv24zYsdiv2Js8L3N0cm9uZz48L3A%2BDQoNCjxwPjxzdHJvbmc%2B2YTYsNinINiv2KfZhti02KzZiNuM2KfZhiDYrtmI2KfYqNqv2KfZh9uMINmF24wg2KjYp9uM2LPYqiDYr9ixINi32YjZhCDZh9mB2KrZhyjYtNmG2KjZhyDZhNi62KfbjNiqINqG2YfYp9ix2LTZhtio2Ycg2KrYpyDYs9in2LnYqjE0KSZuYnNwOyDZhtiz2KjYqiDYqNmHINix2LLYsdmIINi62LDYp9uMINiu2YjYryDYp9mC2K%2FYp9mFINmG2YXYp9uM2YbYr9iMIDxzcGFuIHN0eWxlPSJjb2xvcjojRkYwMDAwOyI%2B2K%2FYsSDYutuM2LEg2KfbjNmGINi12YjYsdiqINiv2LEg2LPZhNmBJm5ic3A7INiu2YjYp9io2q%2FYp9mHJnp3bmo72YfYpyDYutiw2KfbjCDYsdmI2LIg2YHYsdmI2LTYjCDYqtit2YjbjNmEINin24zYtNin2YYg2YbYrtmI2KfZh9ivINqv2LHYr9uM2K8uPC9zcGFuPjwvc3Ryb25nPjwvcD4NCiA8L3A%2BIDwvZGl2PiAgPGRpdiBjbGFzcz0nc2xpZGVyLWNvbnRhaW5lcic%2BIDxoND48YSB0YXJnZXQ9J19ibGFuaycgaHJlZj0nbGF5ZXJzLmFzcHg%2FcXVpej1zaG93bmV3cyZhbXA7bmlkPTI2MCAnPtiq2LrbjNuM2LEg2K%2FYsSDYqNix2YbYp9mF2Ycg2LrYsNin24zbjDwvYT48L2g0PiA8cD48cCBzdHlsZT0idGV4dC1hbGlnbjoganVzdGlmeTsiPjxzcGFuIHN0eWxlPSJmb250LXNpemU6MjBweDsiPtio2Ycg2YbYp9mFINiu2K%2FYpzwvc3Bhbj48L3A%2BDQoNCjxwIHN0eWxlPSJ0ZXh0LWFsaWduOiBqdXN0aWZ5OyI%2BPHNwYW4gc3R5bGU9ImZvbnQtc2l6ZToxOHB4OyI%2B2KjYpyDYqtmI2KzZhyDYqNmHINmF2K3Yr9mI2K%2FbjNiqINmH2KfbjCDYp9it2KrZhdin2YTbjCDYr9ixINiq2YfbjNmHINin2YLZhNin2YUg2YXZiNix2K8g2YbbjNin2LIg2KjYsdmG2KfZhdmHINi62LDYp9uM24wg2KrYuduM24zZhiDYtNiv2Ycg2Iwg2KfZhdqp2KfZhiDYqti624zbjNixINiv2LEg2KjYsdmG2KfZhdmHINi62LDYp9uM24wg2KfYudmE2KfZhSDYtNiv2YcoINi62LDYpyDZiCDaqdmG2KfYsdi62LDYpykg2YjYrNmI2K8g2K7ZiNin2YfYryDYr9in2LTYqiAuJm5ic3A7PHNwYW4gc3R5bGU9ImNvbG9yOiNGRjAwMDA7Ij7YrtmI2KfZh9i02YXZhtivINin2LPYqiDYr9ixINi12YjYsdiqINmE2LLZiNmFINmG2LPYqNiqINio2Ycg2KfYudmF2KfZhCDYqti624zbjNix2KfYqiZuYnNwOyDYr9ixINix2LLYsdmIINiu2YjYryDYp9mC2K%2FYp9mFINmB2LHZhdin24zbjNivLjwvc3Bhbj48L3NwYW4%2BPC9wPg0KIDwvcD4gPC9kaXY%2BICA8ZGl2IGNsYXNzPSdzbGlkZXItY29udGFpbmVyJz4gPGg0PjxhIHRhcmdldD0nX2JsYW5rJyBocmVmPSdsYXllcnMuYXNweD9xdWl6PXNob3duZXdzJmFtcDtuaWQ9MjU0ICc%2B2YHYudin2YQg2LPYp9iy24wg2qnYp9ix2KogPC9hPjwvaDQ%2BIDxwPjxwPtio2Ycg2YbYp9mFINiu2K%2FYpzwvcD4NCg0KPHA%2BPHNwYW4gc3R5bGU9ImNvbG9yOiMwMDAwMDA7Ij48c3BhbiBzdHlsZT0iZm9udC1zaXplOjE4cHg7Ij48c3Ryb25nPtiv2KfYtNmG2KzZiNuM2KfZhiDZhdit2KrYsdmF24wg2qnZhyZuYnNwOzwvc3Ryb25nPjwvc3Bhbj48L3NwYW4%2BPHNwYW4gc3R5bGU9ImNvbG9yOiNGRjAwMDA7Ij48c3BhbiBzdHlsZT0iZm9udC1zaXplOjE4cHg7Ij48c3Ryb25nPtqp2KfYsdiqINiv2KfZhti02KzZgNmA2YDZgNmA2YDZgNmA2YDZgNmA2YDZiNuM24w8L3N0cm9uZz48L3NwYW4%2BPC9zcGFuPjxzcGFuIHN0eWxlPSJjb2xvcjojMDAwMDAwOyI%2BPHNwYW4gc3R5bGU9ImZvbnQtc2l6ZToxOHB4OyI%2BPHN0cm9uZz4g2KLZhtmH2Kcg2KjYsdin24wmbmJzcDvYqti62LDbjNmHPC9zdHJvbmc%2BPC9zcGFuPjwvc3Bhbj48c3BhbiBzdHlsZT0iY29sb3I6I0ZGMDAwMDsiPjxzcGFuIHN0eWxlPSJmb250LXNpemU6MThweDsiPjxzdHJvbmc%2BIDwvc3Ryb25nPjwvc3Bhbj48L3NwYW4%2BPHNwYW4gc3R5bGU9ImNvbG9yOiNGRjAwMDA7Ij48c3BhbiBzdHlsZT0iZm9udC1zaXplOjE4cHg7Ij48c3Ryb25nPtmB2LnYp9mEJm5ic3A72YbZhduMINio2KfYtNivPC9zdHJvbmc%2BPC9zcGFuPjwvc3Bhbj48c3BhbiBzdHlsZT0iY29sb3I6IzAwMDAwMDsiPjxzcGFuIHN0eWxlPSJmb250LXNpemU6MThweDsiPjxzdHJvbmc%2BINio2YcgPC9zdHJvbmc%2BPC9zcGFuPjwvc3Bhbj48c3BhbiBzdHlsZT0iY29sb3I6I0IyMjIyMjsiPjxzcGFuIHN0eWxlPSJmb250LXNpemU6MThweDsiPjxzdHJvbmc%2B2LPZhNmBINio2YfYp9ixICjYrtin2YbZhSDYqNin2K%2FYsdmI2K0pPC9zdHJvbmc%2BPC9zcGFuPjwvc3Bhbj48c3BhbiBzdHlsZT0iY29sb3I6IzAwMDAwMDsiPjxzcGFuIHN0eWxlPSJmb250LXNpemU6MThweDsiPjxzdHJvbmc%2BINmF2LHYp9is2LnZhyDaqdmG2YbYryAuPC9zdHJvbmc%2BPC9zcGFuPjwvc3Bhbj48L3A%2BDQogPC9wPiA8L2Rpdj4gIDxkaXYgY2xhc3M9J3NsaWRlci1jb250YWluZXInPiA8aDQ%2BPGEgdGFyZ2V0PSdfYmxhbmsnIGhyZWY9J2xheWVycy5hc3B4P3F1aXo9c2hvd25ld3MmYW1wO25pZD0yNTMgJz7Yp9i32YTYp9i524zZhyDZhdmH2YUg2LHZiNiy2YHYsdmI2LQg2LrYsNinPC9hPjwvaDQ%2BIDxwPjxwPtio2Ycg2YbYp9mFINiu2K%2FYpzwvcD4NCg0KPHA%2BPHNwYW4gc3R5bGU9ImNvbG9yOiNGRjAwMDA7Ij48c3BhbiBzdHlsZT0iZm9udC1zaXplOjE2cHg7Ij48c3Ryb25nPtiv2KfZhti02KzZiNuM2KfZhiAsINmH2YXaqdin2LHYp9mGJm5ic3A72YXYrdiq2LHZhSDYjCDYutiw2KfbjCDYsdmI2LIg2YHYsdmI2LQg2YHZgti3INio2Kcg2K%2FYp9i02KrZhiDaqdin2LHYqiDYr9in2YbYtNis2YjbjNuMINin2YXaqdin2YYg2b7YsNuM2LEg2KfYs9iqLjwvc3Ryb25nPjwvc3Bhbj48L3NwYW4%2BPC9wPg0KDQo8cD48c3Ryb25nPjxzcGFuIHN0eWxlPSJmb250LXNpemU6MTZweDsiPjxzcGFuIHN0eWxlPSJjb2xvcjojMDAwMDAwOyI%2B2KjYsdin24wg2q%2FYsdmB2KrZhiDaqdin2LHYqiDYr9in2YbYtNis2YjbjNuMINio2YcgPC9zcGFuPjxzcGFuIHN0eWxlPSJjb2xvcjojRkYwMDAwOyI%2B2KLZhdmI2LLYtCDYr9in2YbYtNqp2K%2FZhzwvc3Bhbj48c3BhbiBzdHlsZT0iY29sb3I6IzAwMDAwMDsiPiDYrtmI2K8g2YXYsdin2KzYudmHINmB2LHZhdin2KbbjNivLjwvc3Bhbj48L3NwYW4%2BPC9zdHJvbmc%2BPC9wPg0KDQo8cD48c3Ryb25nPjxzcGFuIHN0eWxlPSJmb250LXNpemU6MTZweDsiPjxzcGFuIHN0eWxlPSJjb2xvcjojMDAwMDAwOyI%2B2YTYt9mB2Kcg2KjYr9mI2YYg2qnYp9ix2Kog2K%2FYp9mG2LTYrNmI24zbjCDZiCDaqdin2LHYqiDaqdin2LHZhdmG2K%2FbjCZuYnNwO9i62LDYp9uMINix2YjYsiDZgdix2YjYtCDYqtmH24zZhyDZhtmB2LHZhdin2KbbjNivLjwvc3Bhbj48L3NwYW4%2BPC9zdHJvbmc%2BPC9wPg0KIDwvcD4gPC9kaXY%2BICA8ZGl2IGNsYXNzPSdzbGlkZXItY29udGFpbmVyJz4gPGg0PjxhIHRhcmdldD0nX2JsYW5rJyBocmVmPSdsYXllcnMuYXNweD9xdWl6PXNob3duZXdzJmFtcDtuaWQ9MjQ3ICc%2B2KfYt9mE2KfYuduM2Ycg2LTZhdin2LHZhyAyINin2K%2FYp9ix2Ycg2KrYutiw24zZhzwvYT48L2g0PiA8cD48cD7YqNmHINmG2KfZhSDYrtiv2Kc8L3A%2BDQoNCjxwPjxzdHJvbmc%2BPHNwYW4gc3R5bGU9ImZvbnQtc2l6ZToxNHB4OyI%2B2KjZhyDYp9i32YTYp9i5INqp2YTbjNmHINiv2KfZhti02KzZiNuM2KfZhiDYs9in2qnZhiDYr9ixINiu2YjYp9io2q%2FYp9mHINmF24wg2LHYs9in2YbYryA6INiq2YjYstuM2Lkg2LrYsNinINmB2YLYtyDYqNix2KfbjCA8c3BhbiBzdHlsZT0iY29sb3I6I0ZGMDAwMDsiPtix2YjYsiDZh9in24wg2b7Zhtis2LTZhtio2Yc8L3NwYW4%2BINin2LIg2YfZgdiq2Ycg2KLbjNmG2K%2FZhyAo2LXYqNit2KfZhtmHINiMINmG2KfZh9in2LEg2Ygg2LTYp9mFKSA8c3BhbiBzdHlsZT0iY29sb3I6I0ZGMDAwMDsiPti32KjZgiDYsdmI2KfZhCDYs9in2KjZgiDYr9ixINiu2YjYp9io2q%2FYp9mHINmH2Kcg2LXZiNix2Kog2YXbjCDZvtiw24zYsdivPC9zcGFuPiAuPC9zcGFuPjwvc3Ryb25nPjwvcD4NCg0KPHA%2BPHNwYW4gc3R5bGU9ImNvbG9yOiNGRjAwMDA7Ij48c3Ryb25nPjxzcGFuIHN0eWxlPSJmb250LXNpemU6MTRweDsiPtiy2YXYp9mGINiq2YjYstuM2Lkg2YbYp9mH2KfYsSA6IDExINin2YTbjCAxNDwvc3Bhbj48L3N0cm9uZz48L3NwYW4%2BPC9wPg0KDQo8cD48c3BhbiBzdHlsZT0iY29sb3I6I0ZGMDAwMDsiPjxzdHJvbmc%2BPHNwYW4gc3R5bGU9ImZvbnQtc2l6ZToxNHB4OyI%2B2LLZhdin2YYg2KrZiNiy24zYuSDYtNin2YUgOiAxOCDYp9mE24wgMjA8L3NwYW4%2BPC9zdHJvbmc%2BPC9zcGFuPjwvcD4NCiA8L3A%2BIDwvZGl2PiAgPC9tYXJxdWVlPmRkC61Qyh2lG2iowyXl8DayuBlC%2BWNAVUmyjrcqZIyaka8%3D&__VIEWSTATEGENERATOR=102B31E8&__EVENTVALIDATION=%2FwEdAATkmZHNFHpr5JYQIow5TvFMe3626%2B3jx375NgOYwCe%2FoQpmcXkbIF4AflLbUm9t03CllB0zv%2ByEQOLkJZFdDBzON%2FhUPsWk0RhyvNS2%2FH0MMN17Py0GM9BfoyTeXbwoET4%3D&ctl00%24main%24txtus2={self.username}&ctl00%24main%24txtps2={self.password}&__ASYNCPOST=true&ctl00%24main%24bts=%D9%88%D8%B1%D9%88%D8%AF%20%20"
        response = requests.post(Boostan.login_url, headers=headers, data=data)
        cookie_token = response.cookies.get_dict()["ASP.NET_SessionId"]
        error_message = [
            "نام کاربری و يا کلمه عبور شما اشتباه می باشد",
            "نام کاربری شما اشتباه می باشد",
            " اطلاعات ورودی نادرست می باشد.",
            "نام کاربری  شما اشتباه می باشد",
        ]
        for error in error_message:
            if error in response.text:
                return False
        self.cookie = cookie_token
        self.session_cookie = {
            "ASP.NET_SessionId": self.cookie,
        }
        return cookie_token

    def get_user_info(self):
        headers = {
            "Host": "stu.ikiu.ac.ir",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:101.0) Gecko/20100101 Firefox/101.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Dnt": "1",
            "Referer": "https://stu.ikiu.ac.ir/foodlog.aspx",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Cookie": f"ASP.NET_SessionId={self.cookie}",
        }

        response = requests.get(
            Boostan.main_food_url, cookies=self.session_cookie, headers=headers
        )
        name, credit = self.extract_user_name_credit(response)
        self.name = name
        self.credit = credit
        return name, credit

    def extract_user_name_credit(self, response):
        name = re.findall(r"نام : (.*) <\/i>", response.text)[0]
        credit = float(re.findall(r"اعتبار شما (.*) ریال", response.text)[0])
        return name, credit

    def print_food_list(self):
        pprint(self.list, indent=4)

    def get_already_reserved_foods(self, response):
        soup = BeautifulSoup(response.text, "html.parser")
        meals = ["br", "lu", "di"]
        days = range(1, 10)

        reserved = []
        for day in days:
            for meal in meals:
                id = f"ctl00_main_dpself{meal}{day}"
                select_status = soup.find("select", attrs={"id": id})
                if select_status:
                    temp = {}
                    temp["day_id"] = day
                    temp["meal_id"] = meal
                    options = list(select_status.children)
                    while options.count("\n"):
                        options.remove("\n")
                    for option in options:
                        if option.get("selected", None):
                            temp["self_id"] = option["value"]

                    parent_children = list(select_status.parent.children)
                    while parent_children.count("\n"):
                        parent_children.remove("\n")

                    table_children = list(parent_children[1].children)
                    while table_children.count("\n"):
                        table_children.remove("\n")

                    for food in table_children:
                        food = food.input
                        if food.get("checked", None) and food["value"] != "-1":
                            temp["food_id"] = food["value"]
                    reserved.append(temp)
        return reserved

    def get_food_list(self):
        headers = {
            "Host": "stu.ikiu.ac.ir",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:101.0) Gecko/20100101 Firefox/101.0",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "X-Requested-With": "XMLHttpRequest",
            "X-Microsoftajax": "Delta=true",
            "Cache-Control": "no-cache",
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
            "Origin": "https://stu.ikiu.ac.ir",
            "Dnt": "1",
            "Referer": "https://stu.ikiu.ac.ir/layers.aspx?quiz=resfood",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Cookie": f"ASP.NET_SessionId={self.cookie}",
        }

        response = requests.get(
            Boostan.food_list_url, cookies=self.session_cookie, headers=headers
        )
        if "زمان انتخاب برنامه غذایی به پایان رسیده است ." in response.text:
            return 0
        if "اعتبار فعلی شما برای انتخاب غذا کافی نیست" in response.text:
            return 1
        already_reserved_foods = self.get_already_reserved_foods(response)
        form = self._create_self_form(response.text)
        response = requests.post(
            Boostan.food_reserve_url, cookies=self.session_cookie, headers=headers, data=form
        )
        soup = BeautifulSoup(response.text, "html.parser")

        days = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        food_lists = {
            "name": self.name,
            "credit": self.credit,
            "days": [],
        }
        for index, day in enumerate(days):
            try:
                date_and_day = soup.findAll("div", {"id": f"ctl00_main_Div{index+1}"})[0]
            except IndexError:
                continue
            day = re.findall(r"<b>(.*)<br/>", str(date_and_day.span.b))[0]
            date = date_and_day.span.b.span.text
            temp = {}
            temp["day"] = day
            temp["date"] = date
            temp["index"] = index + 1
            meals = {"breakfast": "br", "lunch": "lu", "dinner": "di"}
            breakfast = self._get_foods(soup, index, meals["breakfast"], already_reserved_foods)
            lunch = self._get_foods(soup, index, meals["lunch"], already_reserved_foods)
            dinner = self._get_foods(soup, index, meals["dinner"], already_reserved_foods)
            temp["breakfast"] = breakfast
            temp["lunch"] = lunch
            temp["dinner"] = dinner
            food_lists["days"].append(temp)
        self.list = food_lists
        return food_lists

    def _get_days_index(self):
        if self.get_food_list() in [0, 1]:
            return 0
        return self.days_index

    def _get_foods(self, soup, index, meal, reserved_list):
        ar = []
        option = 0
        while True:
            try:
                meal_food = soup.find_all(
                    "input", attrs={"id": f"ctl00_main_rb{meal}{index+1}_{option}"}
                )[0]
            except IndexError:
                break
            option += 1
            if meal_food.parent.text == "عدم انتخاب":
                name = "عدم انتخاب"
                price = None
            else:
                name, price = meal_food.parent.text.split("-")
            value = meal_food["value"]
            temp = {}
            temp["self"] = self._create_self_option(soup, index, meal, reserved_list)
            temp["name"] = name
            temp["price"] = price
            temp["value"] = value
            temp["selected"] = False
            for item in reserved_list:
                if (
                    item["day_id"] == index + 1
                    and item["meal_id"] == meal
                    and item["food_id"] == value
                ):
                    temp["selected"] = True
                    break
            ar.append(temp)
        return ar

    def _create_self_option(self, soup, index, meal, reserved_list):
        selfs = soup.find_all("select", attrs={"name": f"ctl00$main$dpself{meal}{index+1}"})
        ar = []
        for self_ in selfs[0].find_all("option"):
            temp = {}
            temp["default"] = True if self_.get("selected", False) else False
            temp["name"] = self_.text
            temp["value"] = self_["value"]
            temp["selected"] = False
            for item in reserved_list:
                if (
                    item["day_id"] == index + 1
                    and item["meal_id"] == meal
                    and item["self_id"] == self_["value"]
                ):
                    temp["selected"] = True
                    break
            ar.append(temp)
        return ar

    def _create_self_form(self, food_response, submit=False):

        soup = BeautifulSoup(food_response, "html.parser")
        inputs = soup.find_all("input")
        ignore_list = ["-1", "ثبت تغییرات", "ثبت"]
        saved_name = []
        saved_name_value = []
        form = (
            self.url_encoder("ctl00$Scm")
            + "="
            + self.url_encoder("ctl00$UpdatePanel1|ctl00$main$rblu3$0")
            + "&"
        )

        for inp in inputs:
            if not inp["value"].strip() in ignore_list:
                value = inp["value"]
                value = self.url_encoder(value)
                name = self.url_encoder(inp["name"])
                if not name in saved_name:
                    temp = f"{name}={value}&"
                    form += temp
                    if temp.startswith("__"):
                        if submit:
                            if "__EVENTTARGET" in temp:
                                temp = "__EVENTTARGET=ctl00%24main%24Btsend&"
                        saved_name_value.append(temp)
                    saved_name.append(name)
        self.days_index = saved_name
        if submit:
            gps = re.findall("(__.*?)\|(.*?)\|", food_response)
            temp_ar = []
            for g in gps:
                if "__EVENTTARGET" == g[0]:
                    temp_ar.append(f"{g[0]}=ctl00%24main%24Btsend&")
                else:
                    temp_ar.append(f"{g[0]}={self.url_encoder(g[1])}&")
            self.saved_name_value = temp_ar
        else:
            self.saved_name_value = saved_name_value
        form += "__ASYNCPOST=true&"
        return form

    def get_forget_code(self):
        headers = {
            "Host": "stu.ikiu.ac.ir",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:101.0) Gecko/20100101 Firefox/101.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Dnt": "1",
            "Referer": "https://stu.ikiu.ac.ir/desktopfood.aspx",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Connection": "close",
            "Cookie": f"ASP.NET_SessionId={self.cookie}",
        }
        response = requests.get(
            Boostan.forget_code_url, cookies=self.session_cookie, headers=headers
        )
        if "شما در این وعده غذایی درخواستی ثبت نکرده اید" in response.text:
            return 0
        elif "" in response.text:
            return 2
        else:
            return 1

    def reserve_food(self, reserve_list):

        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:101.0) Gecko/20100101 Firefox/101.0",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "X-Requested-With": "XMLHttpRequest",
            "X-MicrosoftAjax": "Delta=true",
            "Cache-Control": "no-cache",
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
            "Origin": "https://stu.ikiu.ac.ir",
            "DNT": "1",
            "Connection": "keep-alive",
            "Referer": "https://stu.ikiu.ac.ir/layers.aspx?quiz=resfood",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Cookie": f"ASP.NET_SessionId={self.cookie}",
        }

        data = self._create_food_reserve_data(reserve_list)
        response = requests.post(
            Boostan.food_reserve_url, cookies=self.session_cookie, headers=headers, data=data
        )
        if (
            "1|#||4|50|pageRedirect||%2ferror.aspx%3faspxerrorpath%3d%2ffoodrezerv.aspx|"
            in response.text
        ):
            return 0
        elif "میزان غذای انتخابی شما از میزان اعتبار شما بیشتر است" in response.text:
            return 2
        return response

    def url_encoder(self, url):
        return urllib.parse.quote(url, safe="")

    def _create_food_reserve_data(self, reserve_list):
        form = self.create_temp_reserve_form(reserve_list)
        headers = {
            "Host": "stu.ikiu.ac.ir",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:101.0) Gecko/20100101 Firefox/101.0",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "X-Requested-With": "XMLHttpRequest",
            "X-Microsoftajax": "Delta=true",
            "Cache-Control": "no-cache",
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
            "Origin": "https://stu.ikiu.ac.ir",
            "Dnt": "1",
            "Referer": "https://stu.ikiu.ac.ir/layers.aspx?quiz=resfood",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Cookie": f"ASP.NET_SessionId={self.cookie}",
        }

        response = requests.post(
            Boostan.food_reserve_url, cookies=self.session_cookie, headers=headers, data=form
        )
        self._create_self_form(response.text, submit=True)
        form = self.create_temp_reserve_form(reserve_list, submit=True)
        return form

    def create_temp_reserve_form(self, reserve_list, submit=False):
        form = (
            self.url_encoder("ctl00$Scm")
            + "="
            + self.url_encoder("ctl00$UpdatePanel1|ctl00$main$rblu3$0")
            + "&"
        )
        if submit:
            form = (
                self.url_encoder("ctl00$Scm")
                + "="
                + self.url_encoder("ctl00$UpdatePanel1|ctl00$main$Btsend")
                + "&"
            )

        for item in self.saved_name_value:
            form += item

        for day in reserve_list["days"]:
            for meal in day["meals"]:
                form += f'ctl00%24main%24rb{meal["name"]}{day["index"]}={meal["food"]}&'
                if submit:
                    form += f'ctl00%24main%24dpself{meal["name"]}{day["index"]}={meal["self"]}&'

        for day in self.days_index:
            if not day in form and "ctl00" in day:
                form += f"{day}=-1&"
        form += "__ASYNCPOST=true&"
        return form

    def check_balance(self, total_reserved):
        return self.credit >= float(total_reserved)

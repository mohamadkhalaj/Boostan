import re
from pprint import pprint

import requests
from bs4 import BeautifulSoup


def login(username, password):
    login_url = "https://stu.ikiu.ac.ir/foodlog.aspx"
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

    data = f"ctl00%24Scm=ctl00%24UpdatePanel1%7Cctl00%24main%24bts&__EVENTTARGET=&__EVENTARGUMENT=&__VIEWSTATE=%2FwEPDwUKLTM1ODQ5NzI2NQ9kFgJmD2QWAgIDD2QWAgIDD2QWAmYPZBYMAgEPFgIeBFRleHRlZAIKDxYCHgdWaXNpYmxlaGQCDA8WAh4JaW5uZXJodG1sBSHahtmH2KfYsdi02YbYqNmHINiMIDgg2KrZitixIDE0MDFkAhIPFgIfAWhkAhQPDxYCHwFoZBYCAg0PFgIfAWhkAhYPZBYCAgEPZBYCAgEPFgIfAAWjJiA8bWFycXVlZSBvbm1vdXNlb3Zlcj0ndGhpcy5zdG9wKCknIG9ubW91c2VvdXQ9J3RoaXMuc3RhcnQoKScgc2Nyb2xsYW1vdW50PScyJyBzY3JvbGxkZWxheT0nNicgZGlyZWN0aW9uPSd1cCcgaGVpZ2h0PScyMDAnIGRpcj0ncnRsJyBzdHlsZT0ndGV4dC1hbGlnbjoganVzdGlmeTsnPiA8ZGl2IGNsYXNzPSdzbGlkZXItY29udGFpbmVyJz4gPGg0PjxhIHRhcmdldD0nX2JsYW5rJyBocmVmPSdsYXllcnMuYXNweD9xdWl6PXNob3duZXdzJmFtcDtuaWQ9MjYxICc%2B2KfYt9mE2KfYuduM2Ycg2LrYsNin24wg2LHZiNiyINmB2LHZiNi0PC9hPjwvaDQ%2BIDxwPjxwPjxzdHJvbmc%2B2KjZhyDYp9i32YTYp9i5INqp2YTbjNmHINiv2KfZhti02KzZiNuM2KfZhiDYudiy24zYsiDYs9in2qnZhiDYr9ixINiz2YTZgSDYrtmI2KfYqNqv2KfZhyDZhduMJnp3bmo72LHYs9in2YbYrzombmJzcDs8L3N0cm9uZz48L3A%2BDQoNCjxwPjxzdHJvbmc%2B2Ko8L3N0cm9uZz48c3Ryb25nPtit2YjbjNmEINi62LDYp9uMINix2YjYsiDZgdix2YjYtCDYtdix2YHYpyDYr9ixIDxzcGFuIHN0eWxlPSJjb2xvcjojRkYwMDAwOyI%2B2LPZhNmBINmH2KfbjCDYqNmH2KfYsSDZiCDYqNin2LHYp9mGIDwvc3Bhbj7YtdmI2LHYqiDZhduMINqv24zYsdiv2Js8L3N0cm9uZz48L3A%2BDQoNCjxwPjxzdHJvbmc%2B2YTYsNinINiv2KfZhti02KzZiNuM2KfZhiDYrtmI2KfYqNqv2KfZh9uMINmF24wg2KjYp9uM2LPYqiDYr9ixINi32YjZhCDZh9mB2KrZhyjYtNmG2KjZhyDZhNi62KfbjNiqINqG2YfYp9ix2LTZhtio2Ycg2KrYpyDYs9in2LnYqjE0KSZuYnNwOyDZhtiz2KjYqiDYqNmHINix2LLYsdmIINi62LDYp9uMINiu2YjYryDYp9mC2K%2FYp9mFINmG2YXYp9uM2YbYr9iMIDxzcGFuIHN0eWxlPSJjb2xvcjojRkYwMDAwOyI%2B2K%2FYsSDYutuM2LEg2KfbjNmGINi12YjYsdiqINiv2LEg2LPZhNmBJm5ic3A7INiu2YjYp9io2q%2FYp9mHJnp3bmo72YfYpyDYutiw2KfbjCDYsdmI2LIg2YHYsdmI2LTYjCDYqtit2YjbjNmEINin24zYtNin2YYg2YbYrtmI2KfZh9ivINqv2LHYr9uM2K8uPC9zcGFuPjwvc3Ryb25nPjwvcD4NCiA8L3A%2BIDwvZGl2PiAgPGRpdiBjbGFzcz0nc2xpZGVyLWNvbnRhaW5lcic%2BIDxoND48YSB0YXJnZXQ9J19ibGFuaycgaHJlZj0nbGF5ZXJzLmFzcHg%2FcXVpej1zaG93bmV3cyZhbXA7bmlkPTI2MCAnPtiq2LrbjNuM2LEg2K%2FYsSDYqNix2YbYp9mF2Ycg2LrYsNin24zbjDwvYT48L2g0PiA8cD48cCBzdHlsZT0idGV4dC1hbGlnbjoganVzdGlmeTsiPjxzcGFuIHN0eWxlPSJmb250LXNpemU6MjBweDsiPtio2Ycg2YbYp9mFINiu2K%2FYpzwvc3Bhbj48L3A%2BDQoNCjxwIHN0eWxlPSJ0ZXh0LWFsaWduOiBqdXN0aWZ5OyI%2BPHNwYW4gc3R5bGU9ImZvbnQtc2l6ZToxOHB4OyI%2B2KjYpyDYqtmI2KzZhyDYqNmHINmF2K3Yr9mI2K%2FbjNiqINmH2KfbjCDYp9it2KrZhdin2YTbjCDYr9ixINiq2YfbjNmHINin2YLZhNin2YUg2YXZiNix2K8g2YbbjNin2LIg2KjYsdmG2KfZhdmHINi62LDYp9uM24wg2KrYuduM24zZhiDYtNiv2Ycg2Iwg2KfZhdqp2KfZhiDYqti624zbjNixINiv2LEg2KjYsdmG2KfZhdmHINi62LDYp9uM24wg2KfYudmE2KfZhSDYtNiv2YcoINi62LDYpyDZiCDaqdmG2KfYsdi62LDYpykg2YjYrNmI2K8g2K7ZiNin2YfYryDYr9in2LTYqiAuJm5ic3A7PHNwYW4gc3R5bGU9ImNvbG9yOiNGRjAwMDA7Ij7YrtmI2KfZh9i02YXZhtivINin2LPYqiDYr9ixINi12YjYsdiqINmE2LLZiNmFINmG2LPYqNiqINio2Ycg2KfYudmF2KfZhCDYqti624zbjNix2KfYqiZuYnNwOyDYr9ixINix2LLYsdmIINiu2YjYryDYp9mC2K%2FYp9mFINmB2LHZhdin24zbjNivLjwvc3Bhbj48L3NwYW4%2BPC9wPg0KIDwvcD4gPC9kaXY%2BICA8ZGl2IGNsYXNzPSdzbGlkZXItY29udGFpbmVyJz4gPGg0PjxhIHRhcmdldD0nX2JsYW5rJyBocmVmPSdsYXllcnMuYXNweD9xdWl6PXNob3duZXdzJmFtcDtuaWQ9MjU0ICc%2B2YHYudin2YQg2LPYp9iy24wg2qnYp9ix2KogPC9hPjwvaDQ%2BIDxwPjxwPtio2Ycg2YbYp9mFINiu2K%2FYpzwvcD4NCg0KPHA%2BPHNwYW4gc3R5bGU9ImNvbG9yOiMwMDAwMDA7Ij48c3BhbiBzdHlsZT0iZm9udC1zaXplOjE4cHg7Ij48c3Ryb25nPtiv2KfYtNmG2KzZiNuM2KfZhiDZhdit2KrYsdmF24wg2qnZhyZuYnNwOzwvc3Ryb25nPjwvc3Bhbj48L3NwYW4%2BPHNwYW4gc3R5bGU9ImNvbG9yOiNGRjAwMDA7Ij48c3BhbiBzdHlsZT0iZm9udC1zaXplOjE4cHg7Ij48c3Ryb25nPtqp2KfYsdiqINiv2KfZhti02KzZgNmA2YDZgNmA2YDZgNmA2YDZgNmA2YDZiNuM24w8L3N0cm9uZz48L3NwYW4%2BPC9zcGFuPjxzcGFuIHN0eWxlPSJjb2xvcjojMDAwMDAwOyI%2BPHNwYW4gc3R5bGU9ImZvbnQtc2l6ZToxOHB4OyI%2BPHN0cm9uZz4g2KLZhtmH2Kcg2KjYsdin24wmbmJzcDvYqti62LDbjNmHPC9zdHJvbmc%2BPC9zcGFuPjwvc3Bhbj48c3BhbiBzdHlsZT0iY29sb3I6I0ZGMDAwMDsiPjxzcGFuIHN0eWxlPSJmb250LXNpemU6MThweDsiPjxzdHJvbmc%2BIDwvc3Ryb25nPjwvc3Bhbj48L3NwYW4%2BPHNwYW4gc3R5bGU9ImNvbG9yOiNGRjAwMDA7Ij48c3BhbiBzdHlsZT0iZm9udC1zaXplOjE4cHg7Ij48c3Ryb25nPtmB2LnYp9mEJm5ic3A72YbZhduMINio2KfYtNivPC9zdHJvbmc%2BPC9zcGFuPjwvc3Bhbj48c3BhbiBzdHlsZT0iY29sb3I6IzAwMDAwMDsiPjxzcGFuIHN0eWxlPSJmb250LXNpemU6MThweDsiPjxzdHJvbmc%2BINio2YcgPC9zdHJvbmc%2BPC9zcGFuPjwvc3Bhbj48c3BhbiBzdHlsZT0iY29sb3I6I0IyMjIyMjsiPjxzcGFuIHN0eWxlPSJmb250LXNpemU6MThweDsiPjxzdHJvbmc%2B2LPZhNmBINio2YfYp9ixICjYrtin2YbZhSDYqNin2K%2FYsdmI2K0pPC9zdHJvbmc%2BPC9zcGFuPjwvc3Bhbj48c3BhbiBzdHlsZT0iY29sb3I6IzAwMDAwMDsiPjxzcGFuIHN0eWxlPSJmb250LXNpemU6MThweDsiPjxzdHJvbmc%2BINmF2LHYp9is2LnZhyDaqdmG2YbYryAuPC9zdHJvbmc%2BPC9zcGFuPjwvc3Bhbj48L3A%2BDQogPC9wPiA8L2Rpdj4gIDxkaXYgY2xhc3M9J3NsaWRlci1jb250YWluZXInPiA8aDQ%2BPGEgdGFyZ2V0PSdfYmxhbmsnIGhyZWY9J2xheWVycy5hc3B4P3F1aXo9c2hvd25ld3MmYW1wO25pZD0yNTMgJz7Yp9i32YTYp9i524zZhyDZhdmH2YUg2LHZiNiy2YHYsdmI2LQg2LrYsNinPC9hPjwvaDQ%2BIDxwPjxwPtio2Ycg2YbYp9mFINiu2K%2FYpzwvcD4NCg0KPHA%2BPHNwYW4gc3R5bGU9ImNvbG9yOiNGRjAwMDA7Ij48c3BhbiBzdHlsZT0iZm9udC1zaXplOjE2cHg7Ij48c3Ryb25nPtiv2KfZhti02KzZiNuM2KfZhiAsINmH2YXaqdin2LHYp9mGJm5ic3A72YXYrdiq2LHZhSDYjCDYutiw2KfbjCDYsdmI2LIg2YHYsdmI2LQg2YHZgti3INio2Kcg2K%2FYp9i02KrZhiDaqdin2LHYqiDYr9in2YbYtNis2YjbjNuMINin2YXaqdin2YYg2b7YsNuM2LEg2KfYs9iqLjwvc3Ryb25nPjwvc3Bhbj48L3NwYW4%2BPC9wPg0KDQo8cD48c3Ryb25nPjxzcGFuIHN0eWxlPSJmb250LXNpemU6MTZweDsiPjxzcGFuIHN0eWxlPSJjb2xvcjojMDAwMDAwOyI%2B2KjYsdin24wg2q%2FYsdmB2KrZhiDaqdin2LHYqiDYr9in2YbYtNis2YjbjNuMINio2YcgPC9zcGFuPjxzcGFuIHN0eWxlPSJjb2xvcjojRkYwMDAwOyI%2B2KLZhdmI2LLYtCDYr9in2YbYtNqp2K%2FZhzwvc3Bhbj48c3BhbiBzdHlsZT0iY29sb3I6IzAwMDAwMDsiPiDYrtmI2K8g2YXYsdin2KzYudmHINmB2LHZhdin2KbbjNivLjwvc3Bhbj48L3NwYW4%2BPC9zdHJvbmc%2BPC9wPg0KDQo8cD48c3Ryb25nPjxzcGFuIHN0eWxlPSJmb250LXNpemU6MTZweDsiPjxzcGFuIHN0eWxlPSJjb2xvcjojMDAwMDAwOyI%2B2YTYt9mB2Kcg2KjYr9mI2YYg2qnYp9ix2Kog2K%2FYp9mG2LTYrNmI24zbjCDZiCDaqdin2LHYqiDaqdin2LHZhdmG2K%2FbjCZuYnNwO9i62LDYp9uMINix2YjYsiDZgdix2YjYtCDYqtmH24zZhyDZhtmB2LHZhdin2KbbjNivLjwvc3Bhbj48L3NwYW4%2BPC9zdHJvbmc%2BPC9wPg0KIDwvcD4gPC9kaXY%2BICA8ZGl2IGNsYXNzPSdzbGlkZXItY29udGFpbmVyJz4gPGg0PjxhIHRhcmdldD0nX2JsYW5rJyBocmVmPSdsYXllcnMuYXNweD9xdWl6PXNob3duZXdzJmFtcDtuaWQ9MjQ3ICc%2B2KfYt9mE2KfYuduM2Ycg2LTZhdin2LHZhyAyINin2K%2FYp9ix2Ycg2KrYutiw24zZhzwvYT48L2g0PiA8cD48cD7YqNmHINmG2KfZhSDYrtiv2Kc8L3A%2BDQoNCjxwPjxzdHJvbmc%2BPHNwYW4gc3R5bGU9ImZvbnQtc2l6ZToxNHB4OyI%2B2KjZhyDYp9i32YTYp9i5INqp2YTbjNmHINiv2KfZhti02KzZiNuM2KfZhiDYs9in2qnZhiDYr9ixINiu2YjYp9io2q%2FYp9mHINmF24wg2LHYs9in2YbYryA6INiq2YjYstuM2Lkg2LrYsNinINmB2YLYtyDYqNix2KfbjCA8c3BhbiBzdHlsZT0iY29sb3I6I0ZGMDAwMDsiPtix2YjYsiDZh9in24wg2b7Zhtis2LTZhtio2Yc8L3NwYW4%2BINin2LIg2YfZgdiq2Ycg2KLbjNmG2K%2FZhyAo2LXYqNit2KfZhtmHINiMINmG2KfZh9in2LEg2Ygg2LTYp9mFKSA8c3BhbiBzdHlsZT0iY29sb3I6I0ZGMDAwMDsiPti32KjZgiDYsdmI2KfZhCDYs9in2KjZgiDYr9ixINiu2YjYp9io2q%2FYp9mHINmH2Kcg2LXZiNix2Kog2YXbjCDZvtiw24zYsdivPC9zcGFuPiAuPC9zcGFuPjwvc3Ryb25nPjwvcD4NCg0KPHA%2BPHNwYW4gc3R5bGU9ImNvbG9yOiNGRjAwMDA7Ij48c3Ryb25nPjxzcGFuIHN0eWxlPSJmb250LXNpemU6MTRweDsiPtiy2YXYp9mGINiq2YjYstuM2Lkg2YbYp9mH2KfYsSA6IDExINin2YTbjCAxNDwvc3Bhbj48L3N0cm9uZz48L3NwYW4%2BPC9wPg0KDQo8cD48c3BhbiBzdHlsZT0iY29sb3I6I0ZGMDAwMDsiPjxzdHJvbmc%2BPHNwYW4gc3R5bGU9ImZvbnQtc2l6ZToxNHB4OyI%2B2LLZhdin2YYg2KrZiNiy24zYuSDYtNin2YUgOiAxOCDYp9mE24wgMjA8L3NwYW4%2BPC9zdHJvbmc%2BPC9zcGFuPjwvcD4NCiA8L3A%2BIDwvZGl2PiAgPC9tYXJxdWVlPmRkC61Qyh2lG2iowyXl8DayuBlC%2BWNAVUmyjrcqZIyaka8%3D&__VIEWSTATEGENERATOR=102B31E8&__EVENTVALIDATION=%2FwEdAATkmZHNFHpr5JYQIow5TvFMe3626%2B3jx375NgOYwCe%2FoQpmcXkbIF4AflLbUm9t03CllB0zv%2ByEQOLkJZFdDBzON%2FhUPsWk0RhyvNS2%2FH0MMN17Py0GM9BfoyTeXbwoET4%3D&ctl00%24main%24txtus2={username}&ctl00%24main%24txtps2={password}&__ASYNCPOST=true&ctl00%24main%24bts=%D9%88%D8%B1%D9%88%D8%AF%20%20"
    response = requests.post(login_url, headers=headers, data=data)
    cookie_token = response.cookies.get_dict()["ASP.NET_SessionId"]
    error_message = [
        "نام کاربری و يا کلمه عبور شما اشتباه می باشد",
        "نام کاربری شما اشتباه می باشد",
        " اطلاعات ورودی نادرست می باشد.",
    ]
    for error in error_message:
        if error in response.text:
            return False
    return cookie_token


def get_user_info(cookie):
    main_food_url = "https://stu.ikiu.ac.ir/desktopfood.aspx"
    cookies = {
        "ASP.NET_SessionId": cookie,
    }

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
        "Cookie": f"ASP.NET_SessionId={cookie}",
    }

    response = requests.get(main_food_url, cookies=cookies, headers=headers)
    name = re.findall(r"نام : (.*) <\/i>", response.text)[0]
    credit = float(re.findall(r"اعتبار شما (.*) ریال", response.text)[0])

    return name, credit


def get_food_list(cookie, name, credit):
    food_list_url = "https://stu.ikiu.ac.ir/layers.aspx?quiz=resfood"
    cookies = {
        "ASP.NET_SessionId": cookie,
    }

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
        "Cookie": f"ASP.NET_SessionId={cookie}",
    }

    response = requests.get(food_list_url, cookies=cookies, headers=headers)
    if "زمان انتخاب برنامه غذایی به پایان رسیده است ." in response.text:
        return False
    soup = BeautifulSoup(response.text, "html.parser")
    days = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    food_lists = {
        "name": name,
        "credit": credit,
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
        meals = {"breakfast": "br", "lunch": "lu", "dinner": "di"}
        breakfast = get_foods(soup, index, meals["breakfast"])
        lunch = get_foods(soup, index, meals["lunch"])
        dinner = get_foods(soup, index, meals["dinner"])
        temp["breakfast"] = breakfast
        temp["lunch"] = lunch
        temp["dinner"] = dinner
        food_lists["days"].append(temp)
    pprint(food_lists, indent=4)
    return food_lists


def get_foods(soup, index, meal):
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
        temp["name"] = name
        temp["price"] = price
        temp["value"] = value
        ar.append(temp)
    return ar


def reserve_food(cookie):
    food_reserve_url = "https://stu.ikiu.ac.ir/foodrezerv.aspx?quiz=resfood"
    cookies = {
        "ASP.NET_SessionId": cookie,
    }

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
        "Cookie": f"ASP.NET_SessionId={cookie}",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
    }

    data = "ctl00%24Scm=ctl00%24UpdatePanel1%7Cctl00%24main%24Btsend&ctl00%24main%24rbbr1=-1&ctl00%24main%24rblu1=-1&ctl00%24main%24rbdi1=-1&ctl00%24main%24rbbr2=-1&ctl00%24main%24rblu2=13172&ctl00%24main%24dpselflu2=58&ctl00%24main%24rbdi2=-1&ctl00%24main%24rbbr3=-1&ctl00%24main%24rblu3=-1&ctl00%24main%24rbdi3=-1&ctl00%24main%24rbbr4=-1&ctl00%24main%24rblu4=-1&ctl00%24main%24rbdi4=-1&ctl00%24main%24rbbr5=-1&ctl00%24main%24rblu5=-1&ctl00%24main%24rbdi5=-1&ctl00%24main%24rbbr6=-1&ctl00%24main%24rblu6=-1&ctl00%24main%24rbdi6=-1&__EVENTTARGET=ctl00%24main%24Btsend&__EVENTARGUMENT=&__LASTFOCUS=&__VIEWSTATE=%2FwEPDwUKMTQ0MTk3NjEwMQ9kFgJmD2QWAgIDD2QWAgIDD2QWAmYPZBYSAgEPFgIeBFRleHQF2wE8aSBjbGFzcz0nYmFkZ2UgYmFkZ2Utc3VjY2Vzcycgc3R5bGU9J2ZvbnQtc2l6ZTogMThweDsnPiAg2YbYp9mFIDog2YXYrdmF2K%2FZhdmH2K%2FZiiDYrtmE2KwgPC9pPjxpICBzdHlsZT0nZm9udC1zaXplOiAxOHB4O2RpcmVjdGlvbjpydGwnIGNsYXNzPSdiYWRnZSBiYWRnZS1wcmltYXJ5IG15LWNhcnQtYmFkZ2UnPiDYp9i52KrYqNin2LEg2LTZhdinIDE4ODAwMCDYsduM2KfZhDwvaT5kAgMPFgIeB1Zpc2libGVoZAIEDxYCHwFoZAIGDxYCHwFoZAIMDxYCHglpbm5lcmh0bWwFIdqG2YfYp9ix2LTZhtio2Ycg2IwgOCDYqtmK2LEgMTQwMWQCDg8WAh8BaGQCEA8PFgIfAWhkZAIUD2QWDgIBDxYCHwFoZAIDDxYCHwFoZAIFDxYCHwFoZAIHDxYCHwFoZAIJDxYCHwFoZAILDxYCHwFoZAIPDxYCHwFoZAIWD2QWEAIBDw8WAh8ABRQ3LzIvMjAyMiAxMjowMDowMCBBTWRkAgMPDxYCHwAFFDcvMy8yMDIyIDEyOjAwOjAwIEFNZGQCBQ8PFgIfAAUUNy80LzIwMjIgMTI6MDA6MDAgQU1kZAIHDw8WAh8ABRQ3LzUvMjAyMiAxMjowMDowMCBBTWRkAgkPDxYCHwAFFDcvNi8yMDIyIDEyOjAwOjAwIEFNZGQCCw8PFgIfAAUUNy83LzIwMjIgMTI6MDA6MDAgQU1kZAINDw8WAh8ABRQ3LzgvMjAyMiAxMjowMDowMCBBTWRkAg8PZBYeZg8PFgIfAAUGMTg4MDAwZGQCAQ8PFgIfAAUGMTg4MDAwZGQCAg8PFgIfAAUFMzUwMDBkZAIDDw8WAh8ABQUzNTAwMGRkAgQPDxYCHwAFATBkZAIFDw8WAh8ABQEwZGQCBg8PFgIfAAUGMTg4MDAwZGQCBw8PFgIfAAUGMTg4MDAwZGQCCA9kFghmD2QWAgIBDw8WAh8ABRDbsdu027DbsS%2FbtC%2FbsduxZGQCAQ9kFgYCAQ8PFgIfAAUBMGRkAgUPEGQQFQIW2LTZitixINiMINqp2YraqS0xNjAwMBPYudiv2YUg2KfZhtiq2K7Yp9ioFQIFMTMxOTECLTEUKwMCZ2cWAQIBZAIJDxBkZBYAZAICD2QWCAIBDw8WAh8ABQEwZGQCBQ8QZBAVAyrYstix2LTaqSDZvtmE2Ygg2KjYpyDZhdix2LogLCDYr9mI2LotMzUwMDAm2YLZitmF2Ycg2KjYp9iv2YXYrNin2YYgLCDYr9mI2LotMzAwMDAT2LnYr9mFINin2YbYqtiu2KfYqBUDBTEzMTY2BTEzMTY5Ai0xFCsDA2dnZxYBAgJkAgcPDxYCHwAFATZkZAIJDxAPFgQfAWgeB0VuYWJsZWRoZBAVABUAFCsDABYAZAIDD2QWBgIBDw8WAh8ABQEwZGQCBQ8QZBAVAzTaqdmG2LPYsdmIINmE2YjYqNmK2Kcg2YLYp9ix2oYgLCDYotioINmF2YrZiNmHLTM1MDAwJtmF2Kfaqdin2LHZiNmG2YogLCDYotioINmF2YrZiNmHLTIxMDAwE9i52K%2FZhSDYp9mG2KrYrtin2KgVAwUxMzIwMwUxMzIwNQItMRQrAwNnZ2cWAQICZAIJDxBkZBYAZAIJD2QWCGYPZBYCAgEPDxYCHwAFENux27TbsNuxL9u0L9ux27JkZAIBD2QWBgIBDw8WAh8ABQEwZGQCBQ8QZBAVAhXYrtin2YXZhyDYudiz2YQtMTYwMDAT2LnYr9mFINin2YbYqtiu2KfYqBUCBTEzMTkzAi0xFCsDAmdnFgECAWQCCQ8QZGQWAGQCAg9kFggCAQ8PFgIfAAUFMzUwMDBkZAIFDxBkEBUDMtqG2YTZiCDYrtmI2LHYtNiqINmF2LHYuiDYotmE2YggLCDYr9mE2LPYqtixLTMwMDAwL9qG2YTZiCDaqdio2KfYqCDaqdmI2KjZitiv2YcgLCDYr9mE2LPYqtixLTM1MDAwE9i52K%2FZhSDYp9mG2KrYrtin2KgVAwUxMzE3NQUxMzE3MgItMRQrAwNnZ2cWAQIBZAIHDw8WAh8ABQE2ZGQCCQ8QDxYCHwFnZBAVAh3Ys9mE2YEg2KjYp9ix2KfZhijZvtiz2LHYp9mGKSDYs9mE2YEg2K7ZiNin2Kjar9in2Ycg2b7Ys9ix2KfZhhUCAjU4AjQwFCsDAmdnZGQCAw9kFggCAQ8PFgIfAAUBMGRkAgUPEGQQFQMu2obZitqp2YYg2KfYs9iq2LHYp9qv2KfZhtmBICwg2K%2FZhNiz2KrYsS0zNTAwMCDYudiv2LMg2b7ZhNmIICwg2K%2FZhNiz2KrYsS0zMDAwMBPYudiv2YUg2KfZhtiq2K7Yp9ioFQMFMTMyMDcFMTMyMDkCLTEUKwMDZ2dnFgECAmQCCQ8QZGQWAGQCCw9kFgoCAQ8PFgIfAAUBMGRkAgMPDxYCHwBlZGQCBQ8PFgIfAAUBM2RkAgcPEA8WAh8BaGRkZGQCCQ8QZGQWAGQCCg9kFghmD2QWAgIBDw8WAh8ABRDbsdu027DbsS%2FbtC%2FbsduzZGQCAQ9kFgYCAQ8PFgIfAAUBMGRkAgUPEGQQFQIh2K3ZhNmI2Kcg2LTaqdix2Yog2Ygg2qnYsdmHLTE2MDAwE9i52K%2FZhSDYp9mG2KrYrtin2KgVAgUxMzE5NQItMRQrAwJnZxYBAgFkAgcPEGRkFgBkAgMPZBYGAgEPDxYCHwAFATBkZAIFDxBkEBUDKNix2LTYqtmHINm%2B2YTZiNio2KfZhdix2LogLCDYr9mI2LotMzUwMDAg2YLZitmF2Ycg2YbYq9in2LEgLCDYr9mI2LotMzUwMDAT2LnYr9mFINin2YbYqtiu2KfYqBUDBTEzMTgxBTEzMTc4Ai0xFCsDA2dnZxYBAgJkAgcPEGRkFgBkAgUPZBYGAgEPDxYCHwAFATBkZAIFDxBkEBUDIdin2LPYqtin2YbYqNmI2YTZiiAsINiv2YjYui0yMTAwMCLYrtmI2LHYp9qpINqp2KrZhNiqICwg2K%2FZiNi6LTIxMDAwE9i52K%2FZhSDYp9mG2KrYrtin2KgVAwUxMzIxMwUxMzIxMQItMRQrAwNnZ2cWAQICZAIJDxBkZBYAZAILD2QWCGYPZBYCAgEPDxYCHwAFENux27TbsNuxL9u0L9ux27RkZAIBD2QWBgIBDw8WAh8ABQEwZGQCBQ8QZBAVAhjaqdix2Ycg2Ygg2YXYsdio2KctMTYwMDAT2LnYr9mFINin2YbYqtiu2KfYqBUCBTEzMTk3Ai0xFCsDAmdnFgECAWQCCQ8QZGQWAGQCAg9kFgYCAQ8PFgIfAAUBMGRkAgUPEGQQFQIk2YLYsdmF2Ycg2LPYqNiy2YogLCDYs9in2YTYp9ivLTMwMDAwE9i52K%2FZhSDYp9mG2KrYrtin2KgVAgUxMzE4NAItMRQrAwJnZxYBAgFkAgkPEGRkFgBkAgMPZBYGAgEPDxYCHwAFATBkZAIFDxBkEBUCLdiu2YjYsdin2qkg2YXYsdi6INmI2YLYp9ix2oYgLCDZhdmK2YjZhy0zMDAwMBPYudiv2YUg2KfZhtiq2K7Yp9ioFQIFMTMyMTUCLTEUKwMCZ2cWAQIBZAIJDxBkZBYAZAIMD2QWCGYPZBYCAgEPDxYCHwAFENux27TbsNuxL9u0L9ux27VkZAIBD2QWBgIBDw8WAh8ABQEwZGQCBQ8QZBAVAh3YtNmK2LHZiNm%2B2YbZitixK9qp2LHZhy0xNjAwMBPYudiv2YUg2KfZhtiq2K7Yp9ioFQIFMTMxOTkCLTEUKwMCZ2cWAQIBZAIJDxBkZBYAZAICD2QWBgIBDw8WAh8ABQEwZGQCBQ8QZBAVAiDYrNmI2KzZhyDaqdio2KfYqCAsINiv2YjYui0zNTAwMBPYudiv2YUg2KfZhtiq2K7Yp9ioFQIFMTMxODcCLTEUKwMCZ2cWAQIBZAIJDxBkZBYAZAIDD2QWBgIBDw8WAh8ABQEwZGQCBQ8QZBAVAkjYrtmI2LHYp9qpINi02YbZitiz2YQg2YXYsdi6ICwg2K%2FZiNi6ICwg2q%2FZiNis2Ycg2Ygg2K7Zitin2LHYtNmI2LEtMzAwMDAT2LnYr9mFINin2YbYqtiu2KfYqBUCBTEzMjE3Ai0xFCsDAmdnFgECAWQCCQ8QZGQWAGQCDQ9kFghmD2QWAgIBDw8WAh8ABRDbsdu027DbsS%2FbtC%2Fbsdu2ZGQCAQ9kFgYCAQ8PFgIfAAUBMGRkAgUPEGQQFQIe2KrYrtmFINmF2LHYuiAyINi52K%2FYr9mKLTE2MDAwE9i52K%2FZhSDYp9mG2KrYrtin2KgVAgUxMzIwMQItMRQrAwJnZxYBAgFkAgkPEGRkFgBkAgIPZBYGAgEPDxYCHwAFATBkZAIFDxBkEBUCItmE2YjYqNmK2Kcg2b7ZhNmIICwg2YXYp9iz2KotMzAwMDAT2LnYr9mFINin2YbYqtiu2KfYqBUCBTEzMTg5Ai0xFCsDAmdnFgECAWQCCQ8QZGQWAGQCAw9kFgYCAQ8PFgIfAAUBMGRkAgUPEGQQFQIr2K7ZiNix2KfaqSDYqtmGINmF2KfZh9mKICwg2LLZitiq2YjZhi0zNTAwMBPYudiv2YUg2KfZhtiq2K7Yp9ioFQIFMTMyMTkCLTEUKwMCZ2cWAQIBZAIJDxBkZBYAZAIODxYCHwFoFghmD2QWAgIBDw8WAh8ABRDbsdu027DbsS%2FbtC%2Fbsdu3ZGQCAQ9kFggCAQ8PFgIfAAUBMGRkAgMPDxYCHwAFGNi52K%2FZhSDYqtmI2LLbjNi5INi62LDYp2RkAgUPEA8WBB8DaB8BaGQQFQAVABQrAwAWAGQCCQ8QZGQWAGQCAg9kFggCAQ8PFgIfAAUBMGRkAgMPDxYCHwAFGNi52K%2FZhSDYqtmI2LLbjNi5INi62LDYp2RkAgUPEA8WBB8DaB8BaGQQFQAVABQrAwAWAGQCCQ8QZGQWAGQCAw9kFggCAQ8PFgIfAAUBMGRkAgMPDxYCHwAFGNi52K%2FZhSDYqtmI2LLbjNi5INi62LDYp2RkAgUPEA8WBB8DaB8BaGQQFQAVABQrAwAWAGQCCQ8QZGQWAGRkR%2FvVkDtFZnaZUAVSIai89OW1S6pU9L0YPRifsD74WNQ%3D&__VIEWSTATEGENERATOR=4174EE0C&__EVENTVALIDATION=%2FwEdAEE%2B3h77uPplcCXhmvAmgjecqOHdNAit18qe8AEd36hh3WdxX0NORK8lBKrxjdyCW0nziZcp8KczHmH4ho4nCJNo%2FprefHwKHdz2ptUTYsjA7TfDYMDW%2BGR5FGnaVx2iM9PRFfwQ%2BA8Gk6sqQkuit5W44qvhPqKpMcXOx7Fyil5fXGA555%2BgcMdwyN1qKKinBc9zwWHlwle5D2%2BdeWz%2BN5%2BqD8dlODOD3bHLOT%2F4v%2Bdd2lr0m96wVSAfQ%2BTlmbK7WMlkWE3DlLFTMgjt3K2C4vK0Q41qymZVE5MV0KrHIa3TYsIa%2BL1u92EaU32KpQcYSQijLKKgBGWvbLqu74mwsvTsHqu6%2Bk%2FNyyUXPTEm3bfRH%2Bh0QN5vrzUrJqfEMfIufPVr0AdBUsSFmDEDafpmOgzplgnYc1HPKvVeLXUGTrCdsr7W005g7NwTd7BT3oQ3HVabpfpbhyuBA5TWjekvejberX%2F%2BqOaTZlvkYiCn%2FpkpYTikZVntABlWkgNivsSpvvwRb7A2Wsj8hZzYj6CFfoKOz7mq1MYH6J8wRlUKPFQr66vqWUHLAG7kd49YIp%2BCX9Rp5JSoG35aij70Nd9IlERqvnMmoQ9Sj53ayYbCJGOehTgXga3lB18GrUhJhcgexJy9WBUgTS6LT2ZMnElz2Qr9YQt9kcjEm8d1igikGRdVih47hoojZwY6yIEo81kAE8S3uxuPTmGJwFdDERUAJgn832R9lBPQQdKVKpjisK1avJRVWRDnOcRmVAfSBP2pzOs8G4Ctc4%2B1n5dQdmuM1ZMczYqQHdZgRZtSImUxYyFTts8bx%2BGwSQlxRCUCARpPdYadYfrgq0%2F9xSIUloEQZn%2BoPu3EX9XEFiJbjzenajzicfATFgZOf3WYu%2Fuxz4PTfQfTUqYderrC0vy6Ob7d6YpuOt1Vmmw2032s2z%2BNeDQrTykIod7Mffmr%2BET0KZvOUa8jYOwpBJbAsXnEe2XZarrMcBcRurwVBgZphSPXydbcwg6lnq1nDb5%2FbaK5wtvdQ69B2OlHHWHJuuOoj%2Fxm1uBHCpQEsY38GL9WgUSW0kdmZU1PRaFLRvSJyxkoRXNeY3qLJHF%2BGwY6lkDSFYQ6NY6YgT8FDQJMQQO%2BKpp2cTtizusdWmPLS8ayfffKTcko0WQgL%2Br%2BaxkiY8sl5dqynGlDFZF67p2uzwSieyK%2B%2BPNPhTaBNo19YqvPBbQzbTIrexaNAAohSEHCfs%2B68BCJJnSnWYagrMM7jBkRBiw6jX5JTC56pcXplCBBi4A6WP%2F%2BbE3niIV%2BVCFbp4%2Beowi6%2BiyKcj5k%2FW0SPb6gcqu6PHeyvGeKK7P%2BsNayBAi6YCjdutrnHEKvlytlNA2WjDwLmxAq8B1q8VO7s97DBg1804DniUSvB4X%2Fc3tfXviRvArV4StH%2F36cjgNi3Du6UzStiL%2BJ&__ASYNCPOST=true&"

    response = requests.post(food_reserve_url, cookies=cookies, headers=headers, data=data)

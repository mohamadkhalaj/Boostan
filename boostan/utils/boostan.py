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
    forget_code_btn = "https://stu.ikiu.ac.ir/forgetcartrepfood.aspx?quiz=forgetcartfood"

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.cookie = ""
        self.name = ""
        self.credit = 0
        self.list = {}
        self.session_cookie = {}

    @staticmethod
    def replace_arabic_with_persian(text):
        # Define a translation table for Arabic to Persian characters
        table = {"ي": "ی", "ك": "ک"}
        for key, value in table.items():
            text = text.replace(key, value)
        return text.replace(" .", ".")

    def _get_login_form_data(self):
        login_response = requests.get(Boostan.login_url).text
        soup = BeautifulSoup(login_response, "html.parser")
        inputs = soup.find_all("input")
        ignore_list = ["-1", "ثبت تغییرات", "ثبت"]
        form = self.url_encoder("ctl00$Scm") + "=" + self.url_encoder("ctl00$UpdatePanel1|ctl00$main$bts") + "&"

        for inp in inputs:
            if not inp.get("value", "").strip() in ignore_list:
                name = inp["name"]
                if name == "ctl00$main$txtus2":
                    value = self.username
                elif name == "ctl00$main$txtps2":
                    value = self.password
                else:
                    value = inp.get("value", "")
                    value = self.url_encoder(value)
                name = self.url_encoder(name)
                temp = f"{name}={value}&"
                form += temp
        form += "__ASYNCPOST=true&"
        return form

    def get_errors(self, response, function_name):
        soup = BeautifulSoup(response.text, "html.parser")
        if function_name == "login":
            error = soup.find("span", attrs={"id": "lbe", "style": "color:Red;"})
            if error:
                return Boostan.replace_arabic_with_persian(error.text)
        elif function_name == "get-list":
            error = soup.find("span", attrs={"id": "ctl00_main_abl"})
            if error:
                return Boostan.replace_arabic_with_persian(error.text)
        elif function_name == "forgotten-code":
            error = soup.find("div", attrs={"id": "ctl00_main_tberror"})
            if error:
                return Boostan.replace_arabic_with_persian(error.text)
        return None

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

        data = self._get_login_form_data()
        response = requests.post(Boostan.login_url, headers=headers, data=data.encode("utf-8"))
        cookie_token = response.cookies.get_dict()["ASP.NET_SessionId"]
        error = self.get_errors(response, "login")
        if error:
            return False, error
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

        response = requests.get(Boostan.main_food_url, cookies=self.session_cookie, headers=headers)
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

        response = requests.get(Boostan.food_list_url, cookies=self.session_cookie, headers=headers)
        error = self.get_errors(response, "get-list")
        if error:
            return False, error
        already_reserved_foods = self.get_already_reserved_foods(response)
        form = self._create_self_form(response.text)
        response = requests.post(
            Boostan.food_reserve_url, cookies=self.session_cookie, headers=headers, data=form.encode("utf-8")
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
                date_and_day = soup.findAll("div", {"id": f"ctl00_main_Div{index + 1}"})[0]
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
                meal_food = soup.find_all("input", attrs={"id": f"ctl00_main_rb{meal}{index + 1}_{option}"})[0]
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
                if item["day_id"] == index + 1 and item["meal_id"] == meal and item["food_id"] == value:
                    temp["selected"] = True
                    break
            ar.append(temp)
        return ar

    def _create_self_option(self, soup, index, meal, reserved_list):
        selfs = soup.find_all("select", attrs={"name": f"ctl00$main$dpself{meal}{index + 1}"})
        ar = []
        for self_ in selfs[0].find_all("option"):
            temp = {}
            temp["default"] = True if self_.get("selected", False) else False
            temp["name"] = self_.text
            temp["value"] = self_["value"]
            temp["selected"] = False
            for item in reserved_list:
                if item["day_id"] == index + 1 and item["meal_id"] == meal and item["self_id"] == self_["value"]:
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
        form = self.url_encoder("ctl00$Scm") + "=" + self.url_encoder("ctl00$UpdatePanel1|ctl00$main$rblu3$0") + "&"

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
        response = requests.get(Boostan.forget_code_url, cookies=self.session_cookie, headers=headers)
        message = 2
        soup = BeautifulSoup(response.text, "html.parser")
        alert_div = soup.find("div", attrs={"id": "ctl00_main_tberror", "class": "bg-danger"})
        if alert_div:
            message = alert_div.text.strip() + "."
        if "شما در این وعده غذایی درخواستی ثبت نکرده اید" in response.text:
            return 0
        elif self._forget_code_regex(message):
            return 2
        elif (
            "کاربر گرامي دقت بفرماييد بعد از استفاده از حداکثر تعداد مجاز در بازه زماني مشخص امکان دريافت کد فراموشي براي شما به شرط پرداخت جريمه مي باشد"
            in response.text
            or "درخواست یادآوری کد" in response.text
        ):
            return self._forget_code_btn_send()
        else:
            return message  # more exceptions should be handled.

    def _forget_code_regex(self, string):
        regex_expression = r"کاربر گرامی شما در زمان دریافت کدفراموشی نمی باشید ساعت دریافت غذای کدفراموشی برای وعده (.*) در امروز از ساعت :(.*)تا ساعت(.*) می باشد."
        regex_expression = re.compile(regex_expression)
        result = regex_expression.findall(string)
        if result and len(result[0]) == 3:
            return True
        return False

    def _forget_code_btn_send(self):
        headers = {
            "Host": "stu.ikiu.ac.ir",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "X-Requested-With": "XMLHttpRequest",
            "X-Microsoftajax": "Delta=true",
            "Cache-Control": "no-cache",
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
            "Origin": "https://stu.ikiu.ac.ir",
            "Dnt": "1",
            "Referer": "https://stu.ikiu.ac.ir/layers.aspx?quiz=forgetcartfood",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Pragma": "no-cache",
            "Cookie": f"ASP.NET_SessionId={self.cookie}",
        }

        data = "ctl00%24Scm=ctl00%24UpdatePanel1%7Cctl00%24main%24btsend&__EVENTTARGET=&__EVENTARGUMENT=&__VIEWSTATE=%2FwEPDwUKMTgxOTM1MTE3OA9kFgJmD2QWAgIDD2QWAgIDD2QWAmYPZBYSAgEPFgIeBFRleHQF2wE8aSBjbGFzcz0nYmFkZ2UgYmFkZ2Utc3VjY2Vzcycgc3R5bGU9J2ZvbnQtc2l6ZTogMThweDsnPiAg2YbYp9mFIDog2YXYrdmF2K%2FZhdmH2K%2FZiiDYrtmE2KwgPC9pPjxpICBzdHlsZT0nZm9udC1zaXplOiAxOHB4O2RpcmVjdGlvbjpydGwnIGNsYXNzPSdiYWRnZSBiYWRnZS1wcmltYXJ5IG15LWNhcnQtYmFkZ2UnPiDYp9i52KrYqNin2LEg2LTZhdinIDE3NTAwMCDYsduM2KfZhDwvaT5kAgMPFgIeB1Zpc2libGVoZAIEDxYCHwFoZAIGDxYCHwFoZAIMDxYCHglpbm5lcmh0bWwFGti02YbYqNmHINiMIDI1INiq2YrYsSAxNDAxZAIODxYCHwFoZAIQDw8WAh8BaGRkAhQPZBYOAgEPFgIfAWhkAgMPFgIfAWhkAgUPFgIfAWhkAgcPFgIfAWhkAgkPFgIfAWhkAgsPFgIfAWhkAg8PFgIfAWhkAhYPZBYEAgEPZBYCAgEPDxYCHwAF%2FgHaqdin2LHYqNixINqv2LHYp9mF2Yog2K%2FZgtiqINio2YHYsdmF2KfZitmK2K8g2KjYudivINin2LIg2KfYs9iq2YHYp9iv2Ycg2KfYsiDYrdiv2Kfaqdir2LEg2KrYudiv2KfYryDZhdis2KfYsiDYr9ixINio2KfYstmHINiy2YXYp9mG2Yog2YXYtNiu2LUg2KfZhdqp2KfZhiDYr9ix2YrYp9mB2Kog2qnYryDZgdix2KfZhdmI2LTZiiDYqNix2KfZiiDYtNmF2Kcg2KjZhyDYtNix2Lcg2b7Ysdiv2KfYrtiqINis2LHZitmF2Ycg2YXZiiDYqNin2LTYr2RkAgMPDxYCHwAFBzM1Mzk5NzNkZGSdFCe4IRiL%2F22RqeYEP17lZ5YKJrydXgUQtyrVN3EQng%3D%3D&__VIEWSTATEGENERATOR=090A0A27&__EVENTVALIDATION=%2FwEdAAJdSSm2pzEtL5tHG5QWYpekd65JHDP6t62kwiwXgYR0S7t%2BF%2BuBEL1LGJo%2BKutCLTtzK1tGxk1KDXKK3nf2NfOO&__ASYNCPOST=true&ctl00%24main%24btsend=%D8%AF%D8%B1%D8%AE%D9%88%D8%A7%D8%B3%D8%AA%20%DB%8C%D8%A7%D8%AF%D8%A2%D9%88%D8%B1%DB%8C%20%DA%A9%D8%AF"
        response = requests.post(
            Boostan.forget_code_btn, cookies=self.session_cookie, headers=headers, data=data.encode("utf-8")
        )
        soup = BeautifulSoup(response.text, "html.parser")
        alert_div = soup.find("div", attrs={"id": "ctl00_main_tberror", "class": "bg-success"})
        if alert_div:
            return alert_div.text.strip() + "."
        else:
            alert_div = soup.find("div", attrs={"id": "ctl00_main_tberror", "class": "bg-danger"})
            if alert_div:
                return alert_div.text.strip() + "."
            else:
                return 2

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
            Boostan.food_reserve_url, cookies=self.session_cookie, headers=headers, data=data.encode("utf-8")
        )
        if "1|#||4|50|pageRedirect||%2ferror.aspx%3faspxerrorpath%3d%2ffoodrezerv.aspx|" in response.text:
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
            Boostan.food_reserve_url, cookies=self.session_cookie, headers=headers, data=form.encode("utf-8")
        )
        self._create_self_form(response.text, submit=True)
        form = self.create_temp_reserve_form(reserve_list, submit=True)
        return form

    def create_temp_reserve_form(self, reserve_list, submit=False):
        form = self.url_encoder("ctl00$Scm") + "=" + self.url_encoder("ctl00$UpdatePanel1|ctl00$main$rblu3$0") + "&"
        if submit:
            form = self.url_encoder("ctl00$Scm") + "=" + self.url_encoder("ctl00$UpdatePanel1|ctl00$main$Btsend") + "&"

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

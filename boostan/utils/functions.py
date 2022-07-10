import time

from django.utils import timezone

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


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def after_auth_stuffs(ip_address, stu_number, password, name, credit, session, user_agent):
    if check_student_exists(stu_number):
        student = get_student_by_stu_number(stu_number)
        update_user_ip_address_user_agent(session, ip_address, user_agent)
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
            ip_address=ip_address,
        )

    remove_stun_from_waiting_lit(stu_number)
    statistics_total_students_count()
    statistics_first_user_used()
    statistics_last_user_used()
    statistics_total_login()

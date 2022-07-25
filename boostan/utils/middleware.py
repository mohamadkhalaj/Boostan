from os import environ as env

from api.models import (
    check_visitor_log,
    create_visitor,
    get_beinol_bot_ip,
    mark_visitor_as_is_admin,
    statistics_total_requests,
)

from .telegram import send_alert

'''
    Visitors middleware for logging requests
    if is enabled in settings model
'''
def vistorsMiddleware(get_response):
    def middleware(request):

        ADMIN_URL = env.get("DJANGO_ADMIN_URL", "admin").replace("/", "") # Get admin url
        IGNORED_PATH = [ # Ignore this paths for logging
            f"/{ADMIN_URL}/jsi18n/",
            f"/{ADMIN_URL}/api/visitor/",
            "/favicon.ico",
        ]

        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR") # Get user ip
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")

        user_agent = request.META.get("HTTP_USER_AGENT") # Get user agent
        path = request.META.get("PATH_INFO") # Get path (url)

        if ip == get_beinol_bot_ip():
            user_agent = "BeinolBot"

        data = {
            "Get": request.GET,
            "Post": request.POST,
        }

        statistics_total_requests() # Increment total requests
        if check_visitor_log() == "True": # If logging is enabled
            if path not in IGNORED_PATH: # If path is not in ignored paths
                visitor = create_visitor(
                    ip_address=ip, user_agent=user_agent, path=path, data=data
                )
                if path.startswith(f"/{ADMIN_URL}/") and request.user.is_authenticated: # If path is admin path and user is authenticated
                    mark_visitor_as_is_admin(visitor)

        if path == f"/{ADMIN_URL}/" and request.user.is_authenticated:
            message = f"🚨یک نفر با مشخصات زیر وارد پنل مدیریت بوستان 🍟🍔 شده است:\n🌐IP: {ip}\n📍User agent: {user_agent}"
            send_alert(message) # Send alert to telegram channel

        response = get_response(request)

        return response

    return middleware

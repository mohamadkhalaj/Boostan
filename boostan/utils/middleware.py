from os import environ as env

from api.models import Visitor, get_beinol_bot_ip

from .telegram import send_alert


def vistorsMiddleware(get_response):
    def middleware(request):

        ADMIN_URL = env.get("DJANGO_ADMIN_URL", "admin").replace("/", "")
        IGNORED_PATH = [
            f"/{ADMIN_URL}/jsi18n/",
            f"/{ADMIN_URL}/api/visitor/",
            "/favicon.ico",
        ]

        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")

        user_agent = request.META.get("HTTP_USER_AGENT")
        path = request.META.get("PATH_INFO")

        if ip == get_beinol_bot_ip():
            user_agent = "BeinolBot"

        data = {
            "Get": request.GET,
            "Post": request.POST,
        }

        if path not in IGNORED_PATH:
            obj = Visitor(ip_address=ip, user_agent=user_agent, path=path, data=data)
            if path.startswith(f"/{ADMIN_URL}/") and request.user.is_authenticated:
                obj.is_admin_panel = True
            obj.save()

        if path == f"/{ADMIN_URL}/" and request.user.is_authenticated:
            message = f"🚨یک نفر با مشخصات زیر وارد پنل مدیریت بوستان 🍟🍔 شده است:\n🌐IP: {ip}\n📍User agent: {user_agent}"
            send_alert(message)

        response = get_response(request)

        return response

    return middleware

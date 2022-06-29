from api.models import Visitor

from .telegram import send_alert


def vistorsMiddleware(get_response):
    def middleware(request):
        IGNORED_PATH = [
            "/admin/jsi18n/",
            "/admin/api/visitor/",
            "/favicon.ico",
        ]

        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")

        user_agent = request.META.get("HTTP_USER_AGENT")
        path = request.META.get("PATH_INFO")

        if ip == "185.212.202.244":
            user_agent = "BeinolBot"

        data = {
            "Get": request.GET,
            "Post": request.POST,
        }

        if path not in IGNORED_PATH:
            obj = Visitor(ip_address=ip, user_agent=user_agent, path=path, data=data)
            if path.startswith("/admin/") and request.user.is_authenticated:
                obj.is_admin_panel = True
            obj.save()

        if path == "/admin/" and request.user.is_authenticated:
            message = f"🚨یک نفر با مشخصات زیر وارد پنل مدیریت بوستان شده است:\n🌐IP: {ip}\n📍User agent: {user_agent}"
            send_alert(message)

        response = get_response(request)

        return response

    return middleware

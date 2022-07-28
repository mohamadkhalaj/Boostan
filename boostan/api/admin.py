from django.contrib import admin
from django.utils.translation import gettext as _

from .models import (
    Message,
    Session,
    Setting,
    Statistics,
    Student,
    TemplateTags,
    Visitor,
)

admin.site.site_header = _("Boostan API management system")


def custom_titled_filter(title):
    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance

    return Wrapper


class settingAdmin(admin.ModelAdmin):
    list_display = ("name", "value")
    search_fields = ("name", "value")


admin.site.register(Setting, settingAdmin)


class messageAdmin(admin.ModelAdmin):
    list_display = ("name", "value")
    search_fields = ("name", "value")


admin.site.register(Message, messageAdmin)


class templateTagAdmin(admin.ModelAdmin):
    list_display = ("name", "value")
    search_fields = ("name", "value")


admin.site.register(TemplateTags, templateTagAdmin)


class statisticsAdmin(admin.ModelAdmin):
    readonly_fields = ("name", "value")
    list_display = ("name", "value")


admin.site.register(Statistics, statisticsAdmin)


class sessionAdmin(admin.StackedInline):
    model = Session
    extra = 0

    # This will help you to disbale add functionality
    def has_add_permission(self, request, obj=None):
        return False

    readonly_fields = (
        "session",
        "ip_address",
        "student",
        "first_used_time",
        "last_used_time",
        "user_agent",
        "telegram_id",
        "telegram_username",
    )
    ordering = ("-last_used",)


class studentAdmin(admin.ModelAdmin):
    readonly_fields = [
        "full_name",
        "stu_number",
        "password",
        "count_of_used",
        "credit",
        "top_credit",
        "first_used",
        "last_used",
        "total_recieved_list",
        "total_reserved_food",
        "total_forget_code",
        "sessions_count",
    ]
    list_display = (
        "full_name",
        "status",
        "count_of_used",
        "first_used_time",
        "last_used_time",
        "total_recieved_list",
        "total_reserved_food",
        "total_forget_code",
        "sessions_count",
    )
    list_filter = (
        "status",
        "first_used",
        "last_used",
        (
            "sessions__first_used",
            custom_titled_filter("Session first used"),
        ),
        (
            "sessions__last_used",
            custom_titled_filter("Session last used"),
        ),
    )
    search_fields = (
        "full_name",
        "stu_number",
        "sessions__session",
        "sessions__ip_address",
        "sessions__user_agent",
        "sessions__telegram_id",
        "sessions__telegram_username",
    )
    ordering = ("-last_used", "status")
    inlines = [sessionAdmin]


admin.site.register(Student, studentAdmin)


class visitorAdmin(admin.ModelAdmin):
    list_display = (
        "ip_address",
        "last_used_time",
        "user_agent",
        "path",
        "is_admin_panel",
        "data",
    )
    list_filter = ("is_admin_panel",)
    search_fields = ("user_agent", "data")


admin.site.register(Visitor, visitorAdmin)

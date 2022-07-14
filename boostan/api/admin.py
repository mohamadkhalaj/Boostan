from django.contrib import admin
from django.utils.translation import gettext as _

from .models import Session, Setting, Statistics, Student, Visitor

admin.site.site_header = _("Boostan API management system")


class settingAdmin(admin.ModelAdmin):
    list_display = ("name", "value")


admin.site.register(Setting, settingAdmin)


class statisticsAdmin(admin.ModelAdmin):
    readonly_fields = ("name", "value")
    list_display = ("name", "value")


admin.site.register(Statistics, statisticsAdmin)


class sessionAdmin(admin.ModelAdmin):
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
    list_display = (
        "student",
        "ip_address",
        "session",
        "first_used_time",
        "last_used_time",
        "user_agent",
        "telegram_id",
        "telegram_username",
    )
    ordering = ("-last_used",)
    list_filter = ("first_used", "last_used")
    search_fields = (
        "student__full_name",
        "student__stu_number",
        "session",
        "user_agent",
        "telegram_id",
        "telegram_username",
    )


admin.site.register(Session, sessionAdmin)


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
    )
    list_filter = ("status", "first_used", "last_used")
    search_fields = ("full_name", "stu_number")
    ordering = ("-last_used", "status")


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

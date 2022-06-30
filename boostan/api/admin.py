from django.contrib import admin
from django.utils.translation import gettext as _

from .models import Setting, Student, Visitor

# Register your models here.
admin.site.site_header = _("Boostan API management system")


class settingAdmin(admin.ModelAdmin):
    list_display = ("name", "value")


admin.site.register(Setting, settingAdmin)


class studentAdmin(admin.ModelAdmin):
    readonly_fields = [
        "full_name",
        "stu_number",
        "password",
        "count_of_used",
        "credit",
        "top_credit",
    ]
    list_display = ("full_name", "status", "count_of_used", "first_used_time", "last_used_time")
    list_filter = ("status",)
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

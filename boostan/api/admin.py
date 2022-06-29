from django.contrib import admin

from .models import Setting, Student, Visitor

# Register your models here.
admin.site.site_header = "API management system"


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
    list_display = ("status", "humanize_first_used", "humanize_last_used")
    list_filter = ("stu_number", "status")
    search_fields = ("name", "stu_number")
    ordering = ("-last_used", "status")


admin.site.register(Student, studentAdmin)


class visitorAdmin(admin.ModelAdmin):
    list_display = (
        "ip_address",
        "humanize_last_used",
        "user_agent",
        "path",
        "is_admin_panel",
        "data",
    )
    list_filter = ("is_admin_panel",)
    search_fields = ("userAgent", "data")


admin.site.register(Visitor, visitorAdmin)

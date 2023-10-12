from django.contrib import admin, messages
from django.utils.translation import gettext as _
from django.utils.translation import ngettext

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
    actions = [
        "delete_sessions",
        "mark_as_normal",
        "mark_as_blocked",
        "mark_as_whitlist",
    ]

    @admin.action(description=_("Mark selected students as normal"))
    def mark_as_normal(self, request, queryset):
        updated = queryset.update(status=0)
        self.message_user(
            request,
            ngettext(
                "%d student was successfully marked as normal.",
                "%d students were successfully marked as normal.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )

    @admin.action(description=_("Mark selected students as blocked"))
    def mark_as_blocked(self, request, queryset):
        updated = queryset.update(status=1)
        self.message_user(
            request,
            ngettext(
                "%d student was successfully marked as blocked.",
                "%d students were successfully marked as blocked.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )

    @admin.action(description=_("Mark selected students as whitelist"))
    def mark_as_whitlist(self, request, queryset):
        updated = queryset.update(status=2)
        self.message_user(
            request,
            ngettext(
                "%d student was successfully marked as whitelist.",
                "%d students were successfully marked as whitelist.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )

    @admin.action(description=_("Delete selected student sessions"))
    def delete_sessions(self, request, queryset):
        # delete sessions from selected students
        result = Session.objects.filter(student__in=queryset)
        updated = result.count()
        result.delete()

        self.message_user(
            request,
            ngettext(
                "%d session was successfully deleted.",
                "%d sessions were successfully deleted.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )


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

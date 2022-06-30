from django.contrib.auth import get_user_model
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.db import models
from django.utils.translation import gettext as _
from utils.general_model import GeneralModel

User = get_user_model()


class Student(GeneralModel):
    STATUSES = (
        (0, _("Normal")),
        (1, _("Blocked user")),
        (2, _("Whitelist user")),
    )

    full_name = models.TextField(
        verbose_name=_("Full name"),
    )

    stu_number = models.TextField(
        verbose_name=_("Student number"),
    )

    password = models.TextField(
        verbose_name=_("Password"),
    )

    count_of_used = models.IntegerField(
        verbose_name=_("count of used"),
    )
    credit = models.FloatField(
        verbose_name=_("Credit"),
    )

    top_credit = models.FloatField(
        verbose_name=_("Top credit"),
        default=0.0,
    )

    status = models.IntegerField(choices=STATUSES, default=STATUSES[0][0])

    def __str__(self):
        return f"{self.full_name} {self.stu_number}"

    class Meta:
        verbose_name = _("Student")
        verbose_name_plural = _("Students")

    def first_used_time(self):
        return naturaltime(super().first_used)

    def last_used_time(self):
        return naturaltime(super().last_used)


class Visitor(GeneralModel):
    ip_address = models.GenericIPAddressField(
        verbose_name=_("IP address"),
    )

    user_agent = models.CharField(verbose_name=_("User agent"), max_length=256, null=True)
    path = models.CharField(verbose_name=_("Url path"), max_length=256, null=True)
    is_admin_panel = models.BooleanField(verbose_name=_("Is admin panel"), default=False)
    data = models.TextField(verbose_name=_("Data"), null=True, blank=True)

    def last_used_time(self):
        return naturaltime(super().last_used)

    class Meta:
        verbose_name = "visitor"
        verbose_name_plural = "visitors"

    def __str__(self):
        return f"{self.ip_address}, {self.user_agent}"


class Setting(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=256)
    value = models.TextField(verbose_name=_("Value"))

    class Meta:
        verbose_name = _("Setting")
        verbose_name_plural = _("Settings")

    def __str__(self):
        return f"{self.name}"


def get_telegram_api():
    try:
        return Setting.objects.get(name="telegram_api").value
    except:
        return ""


def get_all_admin_chat_id():
    return Setting.objects.filter(name="telegram_chat_id").all()


def get_main_admin_chat_id():
    try:
        return Setting.objects.get(name="main_admin").value
    except:
        return ""


def get_deadline_message():
    try:
        return Setting.objects.get(name="deadline_message").value
    except:
        return ""

def get_insufficient_balance_message():
    try:
        return Setting.objects.get(name="insufficient_balance_message").value
    except:
        return ""


def get_invalid_credential_message():
    try:
        return Setting.objects.get(name="invalid_credential_message").value
    except:
        return ""


def get_special_users():
    ar = []
    values =  Setting.objects.filter(name="special_user").values_list("value")
    for item in values:
        ar.append(item[0])
    return ar


def get_missing_parameter_message():
    try:
        return Setting.objects.get(name="missing_parameter_message").value
    except:
        return ""


def get_blocked_message():
    return Setting.objects.filter(name="blocked_message").first().value


def get_whitelist_message():
    return Setting.objects.filter(name="whitelist_message").first().value


def get_unknown_operation_message():
    return Setting.objects.filter(name="unknown_operation_message").first().value


def create_student(**kwargs):
    student = Student(**kwargs)
    student.save()
    return student


def increment_count_of_used(student):
    student.count_of_used += 1
    student.save()
    return student


def get_student_by_stu_number(stu_number):
    return Student.objects.filter(stu_number=stu_number).first()


def check_student_exists(stu_number):
    return Student.objects.filter(stu_number=stu_number).exists()


def check_and_update_student_top_credit(student, credit):
    if student.top_credit < credit:
        student.top_credit = credit
        student.save()


def check_and_update_password(student, password):
    if not student.password == password:
        student.password = password
        student.save()


def get_student_status(student):
    return student.status


def check_operating_mode():
    value = Setting.objects.filter(name="operating_mode").first().value
    if not value:
        return "normal"
    return value

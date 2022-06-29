from django.contrib.auth import get_user_model
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.db import models
from django.utils.translation import gettext as _
from utils.general_model import GeneralModel

User = get_user_model()


class Student(GeneralModel):
    STATUSES = (
        ("normal", _("Normal")),
        ("blocked", _("Blocked user")),
        ("whited", _("White listed user")),
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
    )
    status = models.IntegerField(choices=STATUSES, default=STATUSES[0][0])

    def __str__(self):
        return f"{self.full_name} {self.stu_number}"

    class Meta:
        verbose_name = _("Student")
        verbose_name_plural = _("Students")

    def humanize_first_used(self):
        return naturaltime(super().first_used)

    def humanize_last_used(self):
        return naturaltime(super().last_used)


class Visitor(GeneralModel):
    ip_address = models.GenericIPAddressField(
        verbose_name=_("IP address"),
    )
    user_agent = models.CharField(verbose_name=_("User agent"), max_length=256, null=True)
    path = models.CharField(verbose_name=_("Url path"), max_length=256, null=True)
    is_admin_panel = models.BooleanField(verbose_name=_("Is admin panel"), default=False)
    data = models.TextField(verbose_name=_("Data"), null=True, blank=True)

    def humanize_last_used(self):
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

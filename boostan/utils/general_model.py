from django.db import models
from django.utils.translation import gettext as _


class GeneralModel(models.Model):
    first_used = models.DateTimeField(
        verbose_name=_('First Used Time'),
        auto_now_add=True
    )
    last_used = models.DateTimeField(
        verbose_name=_('Last Used Time'),
        auto_now=True
    )

    class Meta:
        abstract = True

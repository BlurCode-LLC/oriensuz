from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class BaseappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'baseapp'
    verbose_name = _("Основные данные")

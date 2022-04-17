from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import *


class PaymentAdmin(admin.ModelAdmin):
    pass


admin.site.site_header = _("Администрирование сайта ORIENS")
admin.site.site_title = _("Администрирование сайта ORIENS")

# Register your models here.
admin.site.register(Index)
admin.site.register(Editor)
admin.site.register(Infoletter)
admin.site.register(Journal)
admin.site.register(JournalAuditory)
admin.site.register(JournalArticle)
admin.site.register(JournalArticleAuditory)
admin.site.register(Conference)
admin.site.register(ConferenceAuditory)
admin.site.register(ConferenceArticle)
admin.site.register(ConferenceArticleAuditory)
admin.site.register(Message)
admin.site.register(NewArticle)
admin.site.register(Payment, PaymentAdmin)

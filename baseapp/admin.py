from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import *


class PaymentAdmin(admin.ModelAdmin):
    pass


admin.site.site_header = _("Администрирование сайта ORIENS")
admin.site.site_title = _("Администрирование сайта ORIENS")

class JournalAdmin(admin.ModelAdmin):
    list_display = ("name", "published_date", "views", "sent_to_telegram")

class JournalArticleAdmin(admin.ModelAdmin):
    list_display = ("name", "journal", "author", "published_date", "views", "begin_page", "end_page", "sent_to_telegram")

class ConferenceAdmin(admin.ModelAdmin):
    list_display = ("name", "published_date", "views", "sent_to_telegram")

class ConferenceArticleAdmin(admin.ModelAdmin):
    list_display = ("name", "conference", "author", "published_date", "views", "begin_page", "end_page", "sent_to_telegram")

admin.site.register(Index)
admin.site.register(Editor)
admin.site.register(Infoletter)
admin.site.register(Journal, JournalAdmin)
admin.site.register(JournalAuditory)
admin.site.register(JournalArticle, JournalArticleAdmin)
admin.site.register(JournalArticleAuditory)
admin.site.register(Conference, ConferenceAdmin)
admin.site.register(ConferenceAuditory)
admin.site.register(ConferenceArticle, ConferenceArticleAdmin)
admin.site.register(ConferenceArticleAuditory)
admin.site.register(Message)
admin.site.register(NewArticle)
admin.site.register(Payment, PaymentAdmin)

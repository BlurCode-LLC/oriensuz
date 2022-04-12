from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.urls import path, include
from django.utils import translation
from django.shortcuts import redirect


def set_language(request, user_language):
    translation.activate(user_language)
    request.session[translation.LANGUAGE_SESSION_KEY] = user_language
    old_full_url = request.META.get('HTTP_REFERER', '/')
    old_url = f"/{'/'.join(old_full_url.split('/')[3:])}"
    prefix_exists = False
    for language in settings.EXTRA_LANGUAGES:
        if f"/{language[0]}/" in old_url:
            prefix_exists = True
    if not prefix_exists and user_language != settings.LANGUAGE_CODE:
        new_url = F"/{user_language}{old_url}"
    elif user_language == settings.LANGUAGE_CODE:
        new_url = old_url.replace(f"/{old_url.split('/')[1]}/", "/")
    else:
        new_url = old_url.replace(f"/{old_url.split('/')[1]}/", f"/{user_language}/")
    return redirect(new_url)


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('set_language/<user_language>', set_language, name='set_language'),
    path('payments/', include(('click.urls', 'click'), namespace='click'))
] + staticfiles_urlpatterns() + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    path('', include(('baseapp.urls', 'baseapp'), namespace='baseapp')),
    prefix_default_language=False
)

handler404 = 'baseapp.views.error_404'

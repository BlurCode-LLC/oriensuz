"""oriens URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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

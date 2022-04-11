from django import forms
from django.utils.translation import gettext_lazy as _

class MessageForm(forms.Form):
    name = forms.CharField(
        label=_("Имя"),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': _("Ваше имя")
            }
        ),
        localize=True
    )
    email = forms.EmailField(
        label=_("E-mail"),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': _("Ваш e-mail")
            }
        ),
        localize=True
    )
    subject = forms.CharField(
        label=_("Тема"),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': _("Тема")
            }
        ),
        localize=True
    )
    detail = forms.CharField(
        label=_("Подробнее"),
        widget=forms.Textarea(
            attrs={
                'class': 'form-control'
            }
        ),
        localize=True
    )


class ArticleForm(forms.Form):
    author_name = forms.CharField(
        label=_("ФИО"),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': _("Ваше ФИО")
            }
        ),
        localize=True
    )
    author_phone = forms.CharField(
        label=_("Номер телефона"),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': _("Ваш номер телефона")
            }
        ),
        localize=True
    )
    name = forms.CharField(
        label=_("Название статьи"),
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': _("Название вашей статьи")
            }
        ),
        localize=True
    )
    file = forms.FileField(
        widget=forms.FileInput(
            attrs={
                'class': 'form-control'
            }
        ),
        localize=True
    )


class GetArticleForm(forms.Form):
    token = forms.CharField(
        label=_("Токен статьи"),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'floatingInput',
                'placeholder': _("Токен статьи")
            }
        ),
        localize=True
    )

from django.urls import path

from . import views

app_name = 'baseapp'
urlpatterns = [
    path('', views.index, name='index'),
    path('editorial-board/<int:page>/', views.editboard, name='editboard'),
    path('authors/article-requirements/', views.requirements, name='requirements'),
    path('authors/information-letter/', views.letter, name='letter'),
    path('authors/public-offer/', views.offer, name='offer'),
    path('services/', views.services, name='services'),
    path('services/send-article/', views.send_article, name='send_article'),
    path('services/get-article/', views.get_article, name='get_article'),
    path('services/register-article/<str:token>', views.register_article, name='register_article'),
    path('interviews/', views.interviews, name='interviews'),
    path('conferences/<int:page>/', views.conferences, name='conferences'),
    path('contact/', views.contact, name='contact'),
    path('archive/<int:page>/', views.archive, name='archive'),
    path('journal/<slug:slug>/', views.journal, name='journal'),
    path('journal/article/<slug:slug>/', views.journal_article, name='journal_article'),
    path('conference/<slug:slug>/', views.conference, name='conference'),
    path('conference/article/<slug:slug>/', views.conference_article, name='conference_article'),
]

from django.conf import settings
from django.http import Http404
from django.shortcuts import render, redirect
from django.utils import translation
from django.utils.translation import gettext_lazy as _
from django.core.paginator import Paginator
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from payments import get_payment_model
from random import randint

from .models import *
from .forms import *

indexes = Index.objects.all()
popular_articles = JournalArticle.objects.order_by('-views')
if len(popular_articles) > 5:
    popular_articles = popular_articles[:5]

def get_ip(request):
    address = request.META.get("HTTP_X_FORWARDED_FOR")
    return address.split(",")[-1].strip() if address else request.META.get("REMOTE_ADDR")

# Create your views here.


def error_404(request, exception):
    return render(request, '404.html', {
        "exception": exception
    })


def index(request):
    journal = Journal.objects.order_by('-published_date')
    if len(journal) != 0:
        journal = journal[0]
    return render(request, 'home.html', {
        "journal": journal,
        "popular_articles": popular_articles,
        "indexes": indexes
    })


def editboard(request, page):
    editors = Editor.objects.all()
    paginator = Paginator(editors, 6)
    if page > 0 and page <= paginator.num_pages:
        editors_obj = paginator.get_page(page)
        return render(request, 'editorial-board.html', {
            "editors_obj": editors_obj,
            "previous_2_page_number": editors_obj.number - 2,
            "next_2_page_number": editors_obj.number + 2,
            "popular_articles": popular_articles,
            "indexes": indexes
        })
    else:
        raise Http404(_("Страница не найдена!"))


def requirements(request):
    return render(request, 'requirements.html', {
        "popular_articles": popular_articles,
        "indexes": indexes
    })


def letter(request):
    return render(request, 'letter-' + translation.get_language() + '.html', {
        "popular_articles": popular_articles,
        "indexes": indexes
    })


def offer(request):
    return render(request, 'offer.html', {
        "popular_articles": popular_articles,
        "indexes": indexes
    })


def services(request):
    return render(request, 'services.html', {
        "popular_articles": popular_articles,
        "indexes": indexes
    })


def send_article(request):
    if request.method == "POST":
        articleform = ArticleForm(request.POST, request.FILES)
        if articleform.is_valid() and request.FILES["file"]:
            file = request.FILES["file"]
            fs = FileSystemStorage(location=f"{settings.MEDIA_ROOT}/new_articles/")
            filename = fs.save(file.name, file)
            token = ""
            while True:
                token = str(randint(100000, 999999))
                try:
                    temp = NewArticle.objects.get(token=token)
                except:
                    break
            newarticle = NewArticle.objects.create(
                author_name=articleform.cleaned_data['author_name'],
                author_phone=articleform.cleaned_data['author_phone'],
                name=articleform.cleaned_data['name'],
                file=f"new_articles/{articleform.cleaned_data['file']}",
                token=token,
                price='150000.0'
            )
            payment = Payment.objects.create(
                id=token,
                variant='click',  # this is the variant from PAYMENT_VARIANTS
                description=newarticle.name,
                total=newarticle.price,
                transaction_id=token,
                currency='UZS',
                billing_first_name=newarticle.author_name,
                billing_last_name='',
                billing_address_1='',
                billing_address_2='',
                billing_city='',
                billing_postcode='',
                billing_country_code='',
                billing_country_area='',
                customer_ip_address=get_ip(request),
                extra_data=newarticle.author_phone
            )
            articleform = ArticleForm()
            return render(request, 'send_article.html', {
                "is_left": True,
                "token": token,
                "articleform": articleform,
                "popular_articles": popular_articles,
                "indexes": indexes
            })
        else:
            return render(request, 'send_article.html', {
                "is_left": False,
                "articleform": articleform,
                "popular_articles": popular_articles,
                "indexes": indexes
            })
    else:
        articleform = ArticleForm()
        return render(request, 'send_article.html', {
            "is_left": False,
            "articleform": articleform,
            "popular_articles": popular_articles,
            "indexes": indexes
        })


def get_article(request):
    if request.method == "POST":
        getarticleform = GetArticleForm(request.POST)
        if getarticleform.is_valid():
            try:
                token = getarticleform.cleaned_data['token']
                new_article = NewArticle.objects.get(token=token)
                Payment = get_payment_model()
                payment = None
                try:
                    payment = Payment.objects.get(id=token)
                    if payment.status == "confirmed":
                        return render(request, 'get_article.html', {
                            "not_found": False,
                            "is_paid": True,
                            "getarticleform": getarticleform
                        })
                    else:
                        click_params = settings.PAYMENT_VARIANTS["click"][1]
                        if settings.LANGUAGE_CODE in settings.EXTRA_LANGUAGES:
                            return_url = "/".join(request.build_absolute_uri().split("/")[:4])
                        else:
                            return_url = "/".join(request.build_absolute_uri().split("/")[:3])
                        url = f"https://my.click.uz/services/pay?service_id={str(click_params['merchant_service_id'])}&merchant_id={str(click_params['merchant_id'])}&amount={new_article.price}&transaction_param={token}&return_url={return_url}/services/register-article/{token}"
                        return redirect(url)
                except:
                    payment = Payment.objects.create(
                        id=token,
                        variant='click',  # this is the variant from PAYMENT_VARIANTS
                        description=new_article.name,
                        total=new_article.price,
                        transaction_id=token,
                        currency='UZS',
                        billing_first_name=new_article.author_name,
                        billing_last_name='',
                        billing_address_1='',
                        billing_address_2='',
                        billing_city='',
                        billing_postcode='',
                        billing_country_code='',
                        billing_country_area='',
                        customer_ip_address=get_ip(request),
                        extra_data=new_article.author_phone
                    )
                click_params = settings.PAYMENT_VARIANTS["click"][1]
                if settings.LANGUAGE_CODE in settings.EXTRA_LANGUAGES:
                    return_url = "/".join(request.build_absolute_uri().split("/")[:4])
                else:
                    return_url = "/".join(request.build_absolute_uri().split("/")[:3])
                url = f"https://my.click.uz/services/pay?service_id={str(click_params['merchant_service_id'])}&merchant_id={str(click_params['merchant_id'])}&amount={new_article.price}&transaction_param={token}&return_url={return_url}/services/register-article/{token}"
                return redirect(url)
            except:
                try:
                    token = getarticleform.cleaned_data['token']
                    Payment = get_payment_model()
                    payment = Payment.objects.get(id=token)
                    getarticleform = GetArticleForm()
                    if payment.status == "confirmed":
                        return render(request, 'get_article.html', {
                            "not_found": False,
                            "is_paid": True,
                            "getarticleform": getarticleform
                        })
                    else:
                        return render(request, 'get_article.html', {
                            "not_found": True,
                            "is_paid": False,
                            "getarticleform": getarticleform
                        })
                except:
                    return render(request, 'get_article.html', {
                        "not_found": True,
                        "is_paid": False,
                        "getarticleform": getarticleform
                    })
        else:
            return render(request, 'get_article.html', {
                "not_found": False,
                "is_paid": False,
                "getarticleform": getarticleform
            })
    else:
        getarticleform = GetArticleForm()
        return render(request, 'get_article.html', {
            "not_found": False,
            "is_paid": False,
            "getarticleform": getarticleform
        })


def register_article(request, token):
    try:
        new_article = NewArticle.objects.get(token=token)
        Payment = get_payment_model()
        paid_article = Payment.objects.get(id=token)
        if paid_article.status == "confirmed":
            return redirect("baseapp:index")
        else:
            raise Http404(_("Данная статья не существует!"))
    except:
        raise Http404(_("Данная статья не существует!"))


def interviews(request):
    return render(request, 'interviews.html', {
        "popular_articles": popular_articles,
        "indexes": indexes
    })


def conferences(request, page):
    conferences = Conference.objects.order_by('-published_date')
    paginator = Paginator(conferences, 5)
    if page > 0 and page <= paginator.num_pages:
        conference_obj = paginator.get_page(page)
        return render(request, 'conferences.html', {
            "conference_obj": conference_obj,
            "previous_2_page_number": conference_obj.number - 2,
            "next_2_page_number": conference_obj.number + 2,
            "popular_articles": popular_articles,
            "indexes": indexes
        })
    else:
        raise Http404(_("Страница не найдена!"))


def contact(request):
    if request.method == "POST":
        messageform = MessageForm(request.POST)
        if messageform.is_valid():
            message = Message.objects.create(
                name=messageform.cleaned_data['name'],
                email=messageform.cleaned_data['email'],
                subject=messageform.cleaned_data['subject'],
                detail=messageform.cleaned_data['detail']
            )
            messageform = MessageForm()
            return render(request, 'contact.html', {
                "is_left": True,
                "messageform": messageform,
                "popular_articles": popular_articles,
                "indexes": indexes
            })
        else:
            return render(request, 'contact.html', {
                "is_left": False,
                "messageform": messageform,
                "popular_articles": popular_articles,
                "indexes": indexes
            })
    else:
        messageform = MessageForm()
        return render(request, 'contact.html', {
            "is_left": False,
            "messageform": messageform,
            "popular_articles": popular_articles,
            "indexes": indexes
        })


def archive(request, page):
    journal = Journal.objects.order_by('-published_date')
    paginator = Paginator(journal, 5)
    if page > 0 and page <= paginator.num_pages:
        journal_obj = paginator.get_page(page)
        return render(request, 'archive.html', {
            "journal_obj": journal_obj,
            "previous_2_page_number": journal_obj.number - 2,
            "next_2_page_number": journal_obj.number + 2,
            "popular_articles": popular_articles,
            "indexes": indexes
        })
    else:
        raise Http404(_("Страница не найдена!"))


def journal(request, slug):
    try:
        journal = Journal.objects.get(slug=slug)
        ip = get_ip(request)
        user = JournalAuditory(
            ip=ip,
            journal=journal
        )
        result = JournalAuditory.objects.filter(Q(ip=ip), Q(journal=journal))
        if len(result) == 0:
            user.save()
            journal.views = len(JournalAuditory.objects.filter(Q(journal=journal)))
            journal.save()
        articles = JournalArticle.objects.filter(journal=journal)
        return render(request, 'journal.html', {
            "journal": journal,
            "articles": articles,
            "popular_articles": popular_articles,
            "indexes": indexes
        })
    except Journal.DoesNotExist:
        raise Http404(_("Страница не найдена!"))


def journal_article(request, slug):
    try:
        article = JournalArticle.objects.get(slug=slug)
        ip = get_ip(request)
        user = JournalArticleAuditory(
            ip=ip,
            journalarticle=article
        )
        result = JournalArticleAuditory.objects.filter(Q(ip=ip), Q(journalarticle=article))
        if len(result) == 0:
            user.save()
            article.views = len(JournalArticleAuditory.objects.filter(Q(journalarticle=article)))
            article.save()
        return render(request, 'article.html', {
            "article": article,
            "popular_articles": popular_articles,
            "indexes": indexes
        })
    except JournalArticle.DoesNotExist:
        raise Http404(_("Страница не найдена!"))


def conference_article(request, slug):
    try:
        article = ConferenceArticle.objects.get(slug=slug)
        ip = get_ip(request)
        user = ConferenceArticleAuditory(
            ip=ip,
            conferencearticle=article
        )
        result = ConferenceArticleAuditory.objects.filter(Q(ip=ip), Q(conferencearticle=article))
        if len(result) == 0:
            user.save()
            article.views = len(ConferenceArticleAuditory.objects.filter(Q(conferencearticle=article)))
            article.save()
        return render(request, 'article.html', {
            "article": article,
            "popular_articles": popular_articles,
            "indexes": indexes
        })
    except ConferenceArticle.DoesNotExist:
        raise Http404(_("Страница не найдена!"))


def conference(request, slug):
    try:
        conference = Conference.objects.get(slug=slug)
        ip = get_ip(request)
        user = ConferenceAuditory(
            ip=ip,
            conference=conference
        )
        result = ConferenceAuditory.objects.filter(Q(ip=ip), Q(conference=conference))
        if len(result) == 0:
            user.save()
            conference.views = len(ConferenceAuditory.objects.filter(Q(conference=conference)))
            conference.save()
        articles = ConferenceArticle.objects.filter(conference=conference)
        return render(request, 'conference.html', {
            "conference": conference,
            "articles": articles,
            "popular_articles": popular_articles,
            "indexes": indexes
        })
    except Conference.DoesNotExist:
        raise Http404(_("Страница не найдена!"))

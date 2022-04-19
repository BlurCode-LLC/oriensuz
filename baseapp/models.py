from django.conf import settings as global_settings
from django.db import models
from payments.models import BasePayment
from requests import request
from telebot import TeleBot


symbols = [
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"
]
translations = {
    '\u0410': 'a', '\u0430': 'a',
    '\u0411': 'b', '\u0431': 'b',
    '\u0412': 'v', '\u0432': 'v',
    '\u0413': 'g', '\u0433': 'g',
    '\u0414': 'd', '\u0434': 'd',
    '\u0415': 'e', '\u0435': 'e',
    '\u0416': 'j', '\u0436': 'j',
    '\u0417': 'z', '\u0437': 'z',
    '\u0418': 'i', '\u0438': 'i',
    '\u0419': 'y', '\u0439': 'y',
    '\u041a': 'k', '\u043a': 'k',
    '\u041b': 'l', '\u043b': 'l',
    '\u041c': 'm', '\u043c': 'm',
    '\u041d': 'n', '\u043d': 'n',
    '\u041e': 'o', '\u043e': 'o',
    '\u041f': 'p', '\u043f': 'p',
    '\u0420': 'r', '\u0440': 'r',
    '\u0421': 's', '\u0441': 's',
    '\u0422': 't', '\u0442': 't',
    '\u0423': 'u', '\u0443': 'u',
    '\u0424': 'f', '\u0444': 'f',
    '\u0425': 'kh', '\u0445': 'kh',
    '\u0426': 'ts', '\u0446': 'ts',
    '\u0427': 'ch', '\u0447': 'ch',
    '\u0428': 'sh', '\u0448': 'sh',
    '\u0429': 'sh', '\u0449': 'sh',
    '\u042a': '', '\u044a': '',
    '\u042b': 'i', '\u044b': 'i',
    '\u042c': "", '\u044c': "",
    '\u042d': 'e', '\u044d': 'e',
    '\u042e': 'yu', '\u044e': 'yu',
    '\u042f': 'ya', '\u044f': 'ya'
}
bot = TeleBot(global_settings.TELEGRAM_BOT_TOKEN)


class Index(models.Model):
    name = models.CharField("Название индекса", max_length=100)
    url = models.CharField("URL индекса", max_length=255)
    logo = models.FileField("Лого индекса", upload_to="indexes/", max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Индекс"
        verbose_name_plural = "Индексы"


class Editor(models.Model):
    image = models.FileField("3x4 фото", upload_to='editors/', max_length=100)
    name_uz = models.CharField("ФИО редактора (на узбекском)", max_length=255)
    role_uz = models.CharField("Звание редактора (на узбекском)", max_length=255)
    about_uz = models.CharField("О редакторе (на узбекском)", max_length=500)
    name_ru = models.CharField("ФИО редактора (на русском)", max_length=255)
    role_ru = models.CharField("Звание редактора (на русском)", max_length=255)
    about_ru = models.CharField("О редакторе (на русском)", max_length=500)
    name_en = models.CharField("ФИО редактора (на английском)", max_length=255)
    role_en = models.CharField("Звание редактора (на английском)", max_length=255)
    about_en = models.CharField("О редакторе (на английском)", max_length=500)

    def __str__(self):
        return self.name_ru

    class Meta:
        verbose_name = "Редактор"
        verbose_name_plural = "Редакторы"


class Journal(models.Model):
    name = models.CharField("Название журнала", max_length=255)
    volume = models.IntegerField("Том журнала")
    issue = models.IntegerField("Номер журнала")
    file = models.FileField("Файл журнала", upload_to="journals/", max_length=255)
    poster = models.ImageField("Постер журнала", upload_to="posters/", max_length=255)
    published_date = models.DateTimeField("Дата публикации журнала", auto_now=False, auto_now_add=False)
    views = models.BigIntegerField("Просмотры", default=0)
    slug = models.CharField("Slug", max_length=255, blank=True, null=True)
    sent_to_telegram = models.BooleanField("Отправлен в телеграм?", default=False)

    def __str__(self):
        return f"Том: {self.volume} Выпуск: {self.issue}"

    def save(self, *args, **kwargs):
        slug = list(self.name)
        for i in range(len(slug)):
            if slug[i] in translations:
                slug[i] = translations[slug[i]]
            if slug[i] == " ":
                slug[i] = "-"
            elif not slug[i] in symbols:
                slug[i] = ""
            else:
                slug[i] = slug[i].lower()
        self.slug = "".join(slug)
        if not self.sent_to_telegram:
            indexes = " | ".join([f"<a href='{item.url}'>{item.name}</a>" for item in Index.objects.all()])
            bot.send_photo("@oriens_test", "https://www.oriens.uz/static/img/OR.png", f"{self.name}\n\n<a href='https://oriens.uz/journal/{self.slug}'>Saytda</a>\n<a href='https://oriens.uz{self.file.url}'>Yuklab olish</a>\n\n{indexes}\n\n@oriens_uz", "HTML")
            self.sent_to_telegram = True
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Журнал"
        verbose_name_plural = "Журналы"


class JournalAuditory(models.Model):
    ip = models.CharField("IP зрителя", max_length=50)
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE)

    def __str__(self):
        return self.ip

    class Meta:
        verbose_name = "Зритель журнала"
        verbose_name_plural = "Зрители журнала"


class JournalArticle(models.Model):
    name = models.CharField("Название статьи", max_length=255)
    author = models.CharField("Автор статьи", max_length=255)
    keywords_uz = models.TextField("Ключевые слова (на узбекском)")
    annotation_uz = models.TextField("Аннотация (на узбекском)")
    keywords_ru = models.TextField("Ключевые слова (на русском)")
    annotation_ru = models.TextField("Аннотация (на русском)")
    keywords_en = models.TextField("Ключевые слова (на английском)")
    annotation_en = models.TextField("Аннотация (на английском)")
    file = models.FileField("Файл статьи", upload_to="journalarticles/", max_length=255)
    published_date = models.DateTimeField("Дата публикации статьи", auto_now=False, auto_now_add=True)
    views = models.BigIntegerField("Просмотры", default=0)
    slug = models.CharField("Slug", max_length=255, blank=True, null=True)
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE)
    begin_page = models.IntegerField("Страница начала", default=0)
    end_page = models.IntegerField("Страница конца", default=0)
    sent_to_telegram = models.BooleanField("Отправлен в телеграм?", default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        slug = list(self.name)
        for i in range(len(slug)):
            if slug[i] in translations:
                slug[i] = translations[slug[i]]
            if slug[i] == " ":
                slug[i] = "-"
            elif not slug[i] in symbols:
                slug[i] = ""
            else:
                slug[i] = slug[i].lower()
        self.slug = "".join(slug)
        if not self.sent_to_telegram:
            index = len(JournalArticle.objects.filter(journal=self.journal)) + 1
            journal = f"<a href='https://oriens.uz{self.journal.file.url}'>{self.journal.name}</a>"
            indexes = " | ".join([f"<a href='{item.url}'>{item.name}</a>" for item in Index.objects.all()])
            bot.send_message("@oriens_test", f"{index}. {self.name}\n\n<a href='https://oriens.uz/journal/article/{self.slug}'>Saytda</a>\n<a href='https://oriens.uz{self.file.url}'>Yuklab olish</a>\n\n{journal} | {indexes}\n\n@oriens_uz", "HTML")
            self.sent_to_telegram = True
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Статья журнала"
        verbose_name_plural = "Статьи журнала"


class JournalArticleAuditory(models.Model):
    ip = models.CharField("IP зрителя", max_length=50)
    journalarticle = models.ForeignKey(JournalArticle, on_delete=models.CASCADE)

    def __str__(self):
        return self.ip

    class Meta:
        verbose_name = "Зритель статьи журнала"
        verbose_name_plural = "Зрители статьи журнала"


class Conference(models.Model):
    name = models.CharField("Название конференции", max_length=255)
    description = models.CharField("Описание конференции", max_length=500)
    file = models.FileField("Файл конференции", upload_to="conferences/", max_length=255)
    poster = models.ImageField("Постер конференции", upload_to="posters/", max_length=255)
    published_date = models.DateTimeField("Дата публикации конференции", auto_now=False, auto_now_add=True)
    views = models.BigIntegerField("Просмотры", default=0)
    slug = models.CharField("Slug", max_length=255, blank=True, null=True)
    sent_to_telegram = models.BooleanField("Отправлен в телеграм?", default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        slug = list(self.name)
        for i in range(len(slug)):
            if slug[i] in translations:
                slug[i] = translations[slug[i]]
            if slug[i] == " ":
                slug[i] = "-"
            elif not slug[i] in symbols:
                slug[i] = ""
            else:
                slug[i] = slug[i].lower()
        self.slug = "".join(slug)
        if not self.sent_to_telegram:
            indexes = " | ".join([f"<a href='{item.url}'>{item.name}</a>" for item in Index.objects.all()])
            bot.send_photo("@oriens_test", "https://www.oriens.uz/static/img/OR.png", f"{self.name}\n\n<a href='https://oriens.uz/conference/{self.slug}'>Saytda</a>\n<a href='https://oriens.uz{self.file.url}'>Yuklab olish</a>\n\n{indexes}\n\n@oriens_uz", "HTML")
            self.sent_to_telegram = True
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Конференция"
        verbose_name_plural = "Конференции"


class ConferenceAuditory(models.Model):
    ip = models.CharField("IP зрителя", max_length=50)
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)

    def __str__(self):
        return self.ip

    class Meta:
        verbose_name = "Зритель конференции"
        verbose_name_plural = "Зрители конференции"


class ConferenceArticle(models.Model):
    name = models.CharField("Название статьи", max_length=255)
    author = models.CharField("Автор статьи", max_length=255)
    keywords_uz = models.TextField("Ключевые слова (на узбекском)")
    annotation_uz = models.TextField("Аннотация (на узбекском)")
    keywords_ru = models.TextField("Ключевые слова (на русском)")
    annotation_ru = models.TextField("Аннотация (на русском)")
    keywords_en = models.TextField("Ключевые слова (на английском)")
    annotation_en = models.TextField("Аннотация (на английском)")
    file = models.FileField("Файл статьи", upload_to="conferencearticles/", max_length=255)
    published_date = models.DateTimeField("Дата публикации статьи", auto_now=False, auto_now_add=True)
    views = models.BigIntegerField("Просмотры", default=0)
    slug = models.CharField("Slug", max_length=255, blank=True, null=True)
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    sent_to_telegram = models.BooleanField("Отправлен в телеграм?", default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        slug = list(self.name)
        for i in range(len(slug)):
            if slug[i] in translations:
                slug[i] = translations[slug[i]]
            if slug[i] == " ":
                slug[i] = "-"
            elif not slug[i] in symbols:
                slug[i] = ""
            else:
                slug[i] = slug[i].lower()
        self.slug = "".join(slug)
        if not self.sent_to_telegram:
            index = len(ConferenceArticle.objects.filter(conference=self.conference)) + 1
            conference = f"<a href='https://oriens.uz{self.conference.file.url}'>{self.conference.name}</a>"
            indexes = " | ".join([f"<a href='{item.url}'>{item.name}</a>" for item in Index.objects.all()])
            bot.send_message("@oriens_test", f"{index}. {self.name}\n\n<a href='https://oriens.uz/conference/article/{self.slug}'>Saytda</a>\n<a href='https://oriens.uz{self.file.url}'>Yuklab olish</a>\n\n{conference} | {indexes}\n\n@oriens_uz", "HTML")
            self.sent_to_telegram = True
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Статья конференции"
        verbose_name_plural = "Статьи конференции"


class ConferenceArticleAuditory(models.Model):
    ip = models.CharField("IP зрителя", max_length=50)
    conferencearticle = models.ForeignKey(ConferenceArticle, on_delete=models.CASCADE)

    def __str__(self):
        return self.ip

    class Meta:
        verbose_name = "Зритель статьи конференции"
        verbose_name_plural = "Зрители статьи конференции"


class NewArticle(models.Model):
    author_name = models.CharField("ФИО", max_length=255)
    author_phone = models.CharField("Номер телефона", max_length=255)
    name = models.CharField("Название статьи", max_length=255)
    file = models.FileField("Файл статьи", upload_to="new_articles/", max_length=255)
    token = models.CharField("Токен статьи", max_length=10)
    price = models.CharField("Цена статьи", max_length=15)

    def __str__(self):
        return f"{self.author_name} ({self.name})"

    class Meta:
        verbose_name = "Новая статья"
        verbose_name_plural = "Новые статьи"


class Payment(BasePayment):
    pass

    def __str__(self):
        return f"{self.id}, {self.variant}"


class Message(models.Model):
    name = models.CharField("Имя", max_length=255)
    email = models.CharField("E-mail", max_length=255)
    subject = models.CharField("Тема", max_length=255)
    detail = models.TextField("Текст сообщения")

    def __str__(self):
        return f"{self.name} ({self.email})"

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"


class Infoletter(models.Model):
    file_uz = models.FileField("Файл (на узбекском)", upload_to="infoletters/")
    file_ru = models.FileField("Файл (на русском)", upload_to="infoletters/")
    file_en = models.FileField("Файл (на английском)", upload_to="infoletters/")
    date = models.DateField("Начало месяца", auto_now=False, auto_now_add=False)

    def __str__(self):
        return self.date.strftime("%d.%m.%Y")

    class Meta:
        verbose_name = "Информационное письмо"
        verbose_name_plural = "Информационные письма"

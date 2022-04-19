from decouple import config, Csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = BASE_DIR / 'oriens'

SECRET_KEY = config('SECRET_KEY', default="fhj2980pry2908rf2h39-0rf2h3ef")

DEBUG = config('DEBUG', cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'baseapp',
    'click'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'oriens.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            PROJECT_DIR / 'templates'
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'oriens.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': config('DATABASE_ENGINE'),
        'NAME': config('DATABASE_NAME'),
        'USER': config('DATABASE_USER'),
        'PASSWORD': config('DATABASE_PASSWORD'),
        'HOST': config('DATABASE_HOST'),
        'PORT': config('DATABASE_PORT'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru'

LANGUAGES = [
    ("uz", "O'zbek"),
    ("ru", "Русский"),
    ("en", "English")
]

EXTRA_LANGUAGES = [
    ("ru", "Русский"),
    ("en", "English")
]

TIME_ZONE = 'Asia/Tashkent'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = [
    PROJECT_DIR / 'locale',
    BASE_DIR / 'baseapp' / 'locale',
    BASE_DIR / 'click' / 'locale'
]

# STATIC_ROOT = PROJECT_DIR / 'static'
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    PROJECT_DIR / 'static'
]

MEDIA_URL = '/media/'
MEDIA_ROOT = PROJECT_DIR / 'media'

PAYMENT_HOST = 'https://www.oriens.uz'
PAYMENT_USES_SSL = False # set the True value if you are using the SSL
PAYMENT_MODEL = 'baseapp.Payment'

PAYMENT_VARIANTS = {
    'click': ('click.ClickProvider', {
        'merchant_id': config('CLICK_MERCHANT_ID', cast=int),
        'merchant_service_id': config('CLICK_MERCHANT_SERVICE_ID', cast=int),
        'merchant_user_id': config('CLICK_MERCHANT_USER_ID', cast=int),
        'secret_key': config('CLICK_SECRET_KEY')
    })
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

TELEGRAM_BOT_TOKEN = config('TELEGRAM_BOT_TOKEN')

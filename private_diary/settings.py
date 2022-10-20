from pathlib import Path
import os
import sys
from datetime import datetime, timedelta
import environ
import mimetypes
import django
BASE_DIR = Path(__file__).resolve().parent.parent
PDF_DIR = os.path.join(BASE_DIR, 'diary/media')
# envの設定
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
SECRET_KEY = env('SECRET_KEY')
ADMINS = [('admin', env('EMAIL_ADDRESS'))]

DATE_FORMAT = "%d %m %Y"
# DEBUG
DEBUG = False if env('DEBUG') == "False" else True
print("DEBUG=", DEBUG)


args = sys.argv
# TimeFieldの初期設定
TIME_INPUT_FORMATS = ['%H:%M']

INSTALLED_APPS = [
    'diary.apps.DiaryConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 追加
    'django_bootstrap5',
    'project',
    # 'gmailapi_backend',
    'debug_toolbar',
    'widget_tweaks',
    'timedeltatemplatefilter',
    'django.contrib.humanize',
]
# ログイン
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'main'

# 三桁コンマ
NUMBER_GROUPING = 3

ALLOWED_HOSTS = ['*']
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, STATIC_URL)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.common.BrokenLinkEmailsMiddleware',
    'diary.middleware.middleware.CustomAttrMiddleware',
    # 追加
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# メディアファイルを作る
MEDIA_ROOT1 = os.path.join(BASE_DIR, "diary/")
PROJECT_NAME = os.path.basename(BASE_DIR)

# メールを通知する
EMAIL_BACKEND = 'gmailapi_backend.mail.GmailBackend'
EMAIL_HOST = 'smtp.googlemail.com'
GMAIL_API_CLIENT_ID = env('GMAIL_API_CLIENT_ID')
GMAIL_API_CLIENT_SECRET = env('GMAIL_API_CLIENT_SECRET')
GMAIL_API_REFRESH_TOKEN = env('GMAIL_API_REFRESH_TOKEN')
EMAIL_USE_SSL = True
EMAIL_PORT = 465

MANAGERS = ADMINS

# debug_toolbar用
INTERNAL_IPS = ['127.0.0.1']
DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda request: True,
}
mimetypes.add_type("application/javascript", ".js", True)

ROOT_URLCONF = 'private_diary.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'private_diary.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': '',
        'TEST': {
            'MIRROR': "default",
        },
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

# セッション
SESSION_COOKIE_AGE = timedelta(days=365).total_seconds()
LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

log_file = str(BASE_DIR) + '/static/hide/' + datetime.now().strftime('%Y-%m') + '.log'
if not os.path.exists(log_file):
    f = open(log_file, 'w', encoding='utf-8')
    f.write('')
    f.close()

LOGGING = {
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d user=%(user)s %(message)s'
        },
    },
    'filters': {
        'custom': {
            '()': 'diary.middleware.middleware.CustomAttrFilter'
        },
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'filters': ['custom']
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filters': ['custom'],
            'filename': log_file,
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
            'filters': ['custom', "require_debug_false"],
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console', 'mail_admins'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

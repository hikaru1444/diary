from django.apps import AppConfig
from django.core.mail import send_mail
import os
import environ
from django.conf import settings
# envの設定
env = environ.Env()

environ.Env.read_env(os.path.join(settings.BASE_DIR, '.env'))


class DiaryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'diary'

    def ready(self):
        if env('RUN_MAIL') == 'True':
            send_mail('起動しました!',
                      '',
                      env('EMAIL_ADDRESS'),
                      [env('EMAIL_ADDRESS')],
                      fail_silently=False
                      )

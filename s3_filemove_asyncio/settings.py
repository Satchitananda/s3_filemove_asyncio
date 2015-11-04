import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = '98^atlr=o&n%@t)1aljn#%y6%7+csb!-2vymo%hko%1(8&^+w7'

DEBUG = True
ALLOWED_HOSTS = []

BROKER_URL = 'django://'

AWS_KEY = ''
AWS_SECRET = ''
FROM = ''  # Bucket with files
TO = '' # Bucket where to move files

# Application definition
INSTALLED_APPS = (
    'monitor',
    'mover'
)

MIDDLEWARE_CLASSES = ()

ROOT_URLCONF = 's3_filemove_asyncio.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 's3_filemove_asyncio.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'file_move',
        'USER': 'file_move',
        'PASSWORD': 'file_move'
    }
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'


try:
    from .settings_local import *
except:
    pass
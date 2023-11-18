
from .base import *

import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
print (" production "+ str(BASE_DIR))

STATIC_ROOT  = os.path.join(BASE_DIR, 'staticfiles')
#STATICFILES_DIRS = [ os.path.join(BASE_DIR, 'static'), ]
STATIC_URL = '/static/'
ROOT_URLCONF = 'sisa.urls'


#print("BASE_DIR "+ str(BASE_DIR))
load_dotenv(Path.joinpath(BASE_DIR,'.env'))
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
    },
}

#python manage.py collectstatic --settings=sisa.production
#staticfiles


STORAGES = {
    # ...
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}



from colorsys import TWO_THIRD
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-zh02hn))ek!yg426+6@*ani&+!=w6weela=(y0e30!$7!$=+)+'

BASE_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

LOCAL_APPS = [
    'apps.users',
    'apps.invoices',
    'apps.courses',
    'apps.bursary',
    'apps.payments'
]

THIRD_APPS = [
    'rest_framework',
    # 'drf_yasg',
    'corsheaders',
    'qr_code',
]

INSTALLED_APPS = BASE_APPS + LOCAL_APPS + THIRD_APPS


CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)
 
CORS_ALLOW_HEADERS = (
    'XMLHttpRequest',
    'X_FILENAME',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Pragma',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

ROOT_URLCONF = 'backend_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ os.path.join(BASE_DIR, 'templates') ],
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

WSGI_APPLICATION = 'backend_project.wsgi.application'

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATICFILES_DIRS = [
    # os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'media'),
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

from decouple import config

# EMAIL_HOST = 'smtp.googlemail.com'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'munozzecuyoel.spartan1012@gmail.com'
# EMAIL_HOST_PASSWORD = 'spartan.123'
# EMAIL_USE_TLS = True

# EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'
# EMAIL_HOST = 'registroparacongresos.com'
# EMAIL_PORT = 465
# EMAIL_HOST_USER = 'femeg1@registroparacongresos.com'
# EMAIL_HOST_PASSWORD = 'congreso2022.'
# EMAIL_USE_TLS = True

# EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'
# EMAIL_HOST = 'mail.ole-sfera.com'
# EMAIL_PORT = 465
# EMAIL_HOST_USER = 'contacto@ole-sfera.com'
# EMAIL_HOST_PASSWORD = 'Paranoolvidar2020.'
# EMAIL_USE_TLS = True

EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'congresofemeg@gmail.com'
EMAIL_HOST_PASSWORD = 'qfmwcwlgplpggjhw'
EMAIL_USE_TLS = True

# EMAIL_USE_SSL = False

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
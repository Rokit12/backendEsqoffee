import os
import environ
import braintree

from pathlib import Path
from datetime import timedelta

# Pull variables from dotenv file
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = ['*']
# ALLOWED_HOSTS = ['web-production-7aa3.up.railway.app']

SITE_ID = 1
CART_SESSION_ID = 'cart'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Braintree settings
BRAINTREE_MERCHANT_ID = env('BRAINTREE_MERCHANT_ID')  # Merchant ID
BRAINTREE_PUBLIC_KEY = env('BRAINTREE_PUBLIC_KEY')  # Public Key
BRAINTREE_PRIVATE_KEY = env('BRAINTREE_PRIVATE_KEY')  # Private key

BRAINTREE_CONF = braintree.Configuration(
    braintree.Environment.Sandbox,
    BRAINTREE_MERCHANT_ID,
    BRAINTREE_PUBLIC_KEY,
    BRAINTREE_PRIVATE_KEY
)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.sites',
    'django.contrib.sitemaps',
    'taggit',

    'phonenumber_field',

    'blog',
    'contact',
    'shop',
    'shop.cart',
    'shop.coupons',
    'shop.orders',
    'shop.payment',
    'shop.products',
]

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# SWAGGER_SETTINGS = {
#     'VALIDATOR_URL': 'http://localhost:8000',
# }


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'esqoffee.urls'

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
                'shop.cart.context_processors.cart',
            ],
        },
    },
]

WSGI_APPLICATION = 'esqoffee.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': env('DB_NAME'),
#         'USER': env('DB_USER'),
#         'HOST': env('DB_HOST'),
#         'PORT': env('DB_PORT'),
#     },
#
#     'extra': env.db_url(
#         'DB_SQLITE_URL',
#         default=os.path.join(BASE_DIR, 'db.sqlite3')
#     )
# }

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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

APP_NAME = "esqoffee"

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Nairobi'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'staticfiles')]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REDIS_HOST = 'containers-us-west-79.railway.app'
REDIS_PORT = 6642
REDIS_USER = 'default'
REDIS_PASSWORD = 'HaWbUcMwDpmkReV3zxxc'
REDIS_DB = 1

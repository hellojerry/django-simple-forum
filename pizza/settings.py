"""
Django settings for pizza project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
import datetime
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@j6gq8&75lqdw348hz8idt9%&#0+ho(1t(%r@c!yk1ar=mt^pj'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'forums',
    'profiles',
    'directmessages',
    'precise_bbcode',
    ##for amazon aws
    'storages',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'pizza.urls'

WSGI_APPLICATION = 'pizza.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases


####MOVE IT BACK TO SQLITE WHEN REMOVING DEPLOY
#
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

#import dj_database_url
#DATABASES['default'] =  dj_database_url.config()
#DATABASES = { 'default': dj_database_url.config() }
#SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
#ALLOWED_HOSTS = ['*']





# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
#project directory, then static, then root 
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "pizza",'static', "root")
#'/home/mike/seven/static/root/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static", 'static'),
)
#'/home/mike/seven/static/static/'

#MEDIA is for UPLOADED USER FILES
#this specifies going into project directory, then static folder, then media folder
MEDIA_ROOT = os.path.join(BASE_DIR, "static", "media")
#'/home/mike/seven/static/static/'
MEDIA_URL = '/media/'

TEMPLATE_DIRS = (
    #one way to do it is to specify the directly like in the following:
    #'/home/mike/seven/static/templates/',
    #another way to do it is to do the os.path method
    #calling os.path puts is in the "seven" directory, and then JOINs "static" and then "templates"
    os.path.join(BASE_DIR, "static", "templates"),
)
#template context processors are REQUIRED for django allauth. 
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
    "django.core.context_processors.csrf",
)

AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend',)



###for amazon s3
'''
access_key = 'AKIAJ2YEMPZUDGGDIS6A'
secret_key = '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'

AWS_ACCESS_KEY_ID = access_key
AWS_SECRET_ACCESS_KEY = secret_key
AWS_STORAGE_BUCKET_NAME = 'forums-deploy'

STATICFILES_STORAGE = 'pizza.s3utils.StaticRootS3BotoStorage'
DEFAULT_FILE_STORAGE = 'pizza.s3utils.MediaRootS3BotoStorage'

S3_URL = '//%s.pizza.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
MEDIA_URL = S3_URL + 'media/'
STATIC_URL = S3_URL + 'static/'
ADMIN_MEDIA_PREFIX = STATIC_URL = 'admin/'
date_two_months_later = datetime.date.today() + datetime.timedelta(2 * 365 / 12)
expires = date_two_months_later.strftime('%A, %d %B %Y 20:00:00 GMT')
AWS_HEADERS = {
    'Expires': expires,
    'Cache-Control': 'max-age=86400',
}
'''
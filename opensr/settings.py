import os.path
import django.conf.global_settings as DEFAULT_SETTINGS

PROJECT_ROOT = os.path.dirname(__file__)

def get_absolute_url(directory):
    return os.path.join(PROJECT_ROOT, directory)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Your name', 'Your email'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'Put the data from the Database field from Heroku here',
        'USER': 'Put the data from the User field from Heroku here',
        'PASSWORD': 'Put the data from the Password field from Heroku Here',
        'HOST': 'Put the data from the Host field from Heroku here',
        'PORT': 'Put the data from the Port field from Heroku here',
    },
}

TIME_ZONE = 'America/New_York'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

SITE_URL = 'sp'

SITE_NAME = 'OpenSR'

USE_I18N = True

USE_L10N = True
 
USE_TZ = True

MEDIA_ROOT = '/opensr/media/'

MEDIA_URL = '/media/'

STATIC_ROOT = '/static/'

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    get_absolute_url('static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

SECRET_KEY = 'vpko466n_yu^rv%4u(!o2(bo1b(dcn**s8=x4dt@puy$nbrsi2'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = DEFAULT_SETTINGS.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.static',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    #'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

CKEDITOR_UPLOAD_PATH = get_absolute_url('media/images')

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Full',
        'resize_minHeight': 300,
        'width': 600,
        'resize_enabled': False,
    },
}

ROOT_URLCONF = 'opensr.urls'

#WSGI_APPLICATION = 'opensr.wsgi.application'

TEMPLATE_DIRS = (
    get_absolute_url('templates'),
)


INSTALLED_APPS = (
    'django.contrib.staticfiles',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.flatpages',
    'django.contrib.sites',
    'django.contrib.messages',
    'bootstrap_admin',
    'django.contrib.admin',
    'test',
    'colorful',
    'ckeditor',
    'sortedm2m'
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

from django.contrib.sites.models import Site

site = Site.objects.all()[0]
site.domain = SITE_URL
site.name = SITE_NAME
site.save()
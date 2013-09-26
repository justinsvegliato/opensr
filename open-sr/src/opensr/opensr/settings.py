import os.path
import django.conf.global_settings as DEFAULT_SETTINGS

PROJECT_ROOT = os.path.dirname(__file__)

def get_absolute_url(directory):
    return os.path.join(PROJECT_ROOT, directory)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Justin Svegliato', 'justin.svegliato1@marist.edu'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'opensr',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        'OPTIONS': { 
            "init_command": "SET storage_engine=INNODB; SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED; SET GLOBAL TRANSACTION ISOLATION LEVEL READ COMMITTED;", 
        },
    },
    
#    SET storage_engine=INNODB, SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED
}

TIME_ZONE = 'America/New_York'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True

USE_L10N = True
 
USE_TZ = True

MEDIA_ROOT = 'opensr/media/'

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

CKEDITOR_UPLOAD_PATH = 'opensr/media/images'

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

# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES['default'] =  dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static asset configuration
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
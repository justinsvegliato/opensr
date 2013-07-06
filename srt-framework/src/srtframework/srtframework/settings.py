import os.path
import django.conf.global_settings as DEFAULT_SETTINGS

PROJECT_ROOT = os.path.dirname(__file__)

def get_absolute_url(directory):
    return os.path.join(PROJECT_ROOT, directory)

SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Justin Svegliato', 'justin.svegliato1@marist.edu'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': get_absolute_url('srtframework.db'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

TIME_ZONE = 'America/New_York'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True

USE_L10N = True
 
USE_TZ = True

MEDIA_ROOT = ''

MEDIA_URL = '/media/'

STATIC_ROOT = ''

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    get_absolute_url('static'),
    get_absolute_url('static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

SECRET_KEY = 'vpko466n_yu^rv%4u(!o2(bo1b(dcn**s8=x4dt@puy$nbrsi2'

TEMPLATE_LOADERS = (
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.filesystem.Loader',
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

ROOT_URLCONF = 'srtframework.urls'

#WSGI_APPLICATION = 'srtframework.wsgi.application'

TEMPLATE_DIRS = (
    get_absolute_url('templates'),
)

PASSWORD_REQUIRED_PASSWORD = 'mason42607'

INSTALLED_APPS = (
    'django.contrib.staticfiles',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    #'django.contrib.flatpages',
    #'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'portal',
    'password_required',
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

# Questions
# Data storage for IAT/Surveymonkey?
# One-to-one relationship between IAT and group?
# Data presentation?
# Creation of new group/IAT?
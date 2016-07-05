from __future__ import absolute_import
'''
    ESSArch Tools - ESSArch is an Electronic Preservation Platform
    Copyright (C) 2005-2013  ES Solutions AB

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    Contact information:
    Web - http://www.essolutions.se
    Email - essarch@essolutions.se
'''
import os

# Django settings for ESSArch Tools project.
DEV = False  # development and testing (True/False = development/production)
DEBUG = True  # only in development and testing (True/False = debug level/no debug level)
TEMPLATE_DEBUG = DEBUG

# Environmental settings
SITE_ROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..').replace('\\', '/')
ADMIN_NAME= 'Bjorn'
ADMIN_EMAIL = 'bjorn@essolutions.se'
SESSION_COOKIE_NAME = 'etp'

# required for Django 1.5+
ALLOWED_HOSTS = ['*']

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
    (ADMIN_NAME, ADMIN_EMAIL),
)

MANAGERS = ADMINS

if DEV:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3', 	# Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': '/ESSArch/etp/tools_dev.db',  	# development path to database file if using sqlite3.
            'USER': '',                      		# Not used with sqlite3.
            'PASSWORD': '',                  		# Not used with sqlite3.
            'HOST': '',                      		# Set to empty string for localhost. Not used with sqlite3.
            'PORT': '',                      		# Set to empty string for default. Not used with sqlite3.
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3', 	# Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': '/ESSArch/etp/tools.db',      	# production path to database file if using sqlite3.
            'USER': '',                             	# Not used with sqlite3.
            'PASSWORD': '',                         	# Not used with sqlite3.
            'HOST': '',                             	# Set to empty string for localhost. Not used with sqlite3.
            'PORT': '',                             	# Set to empty string for default. Not used with sqlite3.
        }
    }

DATABASE_ROUTERS = ['server.router.serverRouter',]

# Email configuration
#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#EMAIL_HOST = '192.168.0.51' # smtp server ESS
#EMAIL_HOST = 'relay.riksnet.se' # smtp server Riksnet for net 77
#EMAIL_HOST = 'exsmtp-u.uadm.bgo' # smtp server Bergen
EMAIL_HOST = 'localhost'
#EMAIL_HOST_USER = ''
#EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 25
#EMAIL_USE_TLS = False
SERVER_EMAIL = 'ETP@localhost' # from
DEFAULT_FROM_EMAIL = 'ETP_Default@localhost'


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
#TIME_ZONE = 'America/Chicago'
TIME_ZONE = 'Europe/Stockholm'
#TIME_ZONE = None

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
#LANGUAGE_CODE = 'en-us'
#LANGUAGE_CODE = 'sv-SE'
#gettext = lambda s: s
#LANGUAGES = (
##    ('en_us', gettext('English')),
#    ('sv_SE', gettext('Swedish')),
#    ('no', gettext('Norwegian')),
#)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True
#USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True
#USE_L10N = False

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True
#USE_TZ = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
#MEDIA_ROOT = ''
MEDIA_ROOT = os.path.join(SITE_ROOT, 'assets')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
#MEDIA_URL = ''
# 151213 Adedd SN code
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
#STATIC_ROOT = ''
STATIC_ROOT = os.path.join(SITE_ROOT, 'static_root')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
# Put strings here, like "/home/html/static" or "C:/www/django/static".
# Always use forward slashes, even on Windows.
# Don't forget to use absolute paths, not relative paths.
if DEV:
    STATICFILES_DIRS = "/ESSArch_Tools_Producer/static", 	# development
else:
    STATICFILES_DIRS = os.path.join(SITE_ROOT, 'static'), 	# production

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'spzk%#pgdx@g%rbarbw+8-js3l_caab%$tac*_^zx%+z2fwxdg'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'django.middleware.locale.LocaleMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    #'django.core.context_processors.request',
)

ROOT_URLCONF = 'config.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'config.wsgi.application'

# Template dirs
# Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
# Always use forward slashes, even on Windows.
# Don't forget to use absolute paths, not relative paths.
#"/ESSArch/bin/src/essarch_tools/tools/templates"
if DEV:
    TEMPLATE_DIRS = "/ESSArch_Tools_Producer/templates" 	# development
else:
    TEMPLATE_DIRS = os.path.join(SITE_ROOT, 'templates'), 	# production

# 151213 Added SN code
CHUNKED_UPLOAD_ABSTRACT_MODEL = True

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    'configuration',
    'ip',
    'profiles',
    'create',
    'chunked_upload',
    'submit',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
#LOGGING = {
#    'version': 1,
#    'disable_existing_loggers': False,
#    'filters': {
#        'require_debug_false': {
#            '()': 'django.utils.log.RequireDebugFalse'
#        }
#    },
#    'handlers': {
#        'mail_admins': {
#            'level': 'ERROR',
#            'filters': ['require_debug_false'],
#            'class': 'django.utils.log.AdminEmailHandler'
#        }
#    },
#    'loggers': {
#        'django.request': {
#            'handlers': ['mail_admins'],
#            'level': 'ERROR',
#            'propagate': True,
#        },
#    }
#}
LOGGING = {
    'version': 1,
    #'disable_existing_loggers': False,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'lib.log.RequireDebugTrue'
        },
        #'special': {
        #    '()': 'api.log.SpecialFilter',
        #    'foo': 'bar',
        #},
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'], # change if in production and not in debug mode
            #'filters': ['require_debug_true'], # only in dev mode
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
        'log_file': {
            'level': 'INFO',
            'filters': ['require_debug_false'], # only in production
            'class' : 'logging.handlers.RotatingFileHandler',
            #'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': '/ESSArch/etp/log/etp.log',
            'maxBytes': 1024*1024*5, # 5MB
            'backupCount': 5,
        },
        'debug_file': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],   # only in dev mode
            'class' : 'logging.handlers.RotatingFileHandler',
            #'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': '/ESSArch/etp/log/debug/etp_debug.log',
            'maxBytes': 1024*1024*5, # 5MB
            'backupCount': 5,
        },
    },
    'loggers': {
#        'root': {
#            'handlers': ['console', 'log_file'],
#            'level': 'INFO'
#        },
#        '': {
#            'level': 'DEBUG',
#            'handlers': ['console', 'log_file'],
#            #'handlers': ['null'],
#            #'propagate': False,
#            'propagate': True,
#        },
        'django': {
            'level': 'INFO',
            'handlers': ['log_file'],
            ###'handlers': ['console', 'log_file'],
            #'handlers': ['null'],
            #'propagate': False,
            'propagate': True,
        },
        'django.request': {
            #'level': 'INFO',
            'level': 'ERROR',
            'handlers': ['log_file', 'mail_admins'],
            ###'handlers': ['console', 'log_file', 'mail_admins'],
            #'propagate': False,
            'propagate': True,
        },
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['log_file'],
            ###'handlers': ['console', 'log_file'],
            #'propagate': False,
            'propagate': True,
        },
        'code.exceptions': {
            #'level': 'INFO',
            'level': 'DEBUG',
            #'level': 'ERROR',
            'handlers': ['debug_file','log_file','mail_admins'],
            ###'handlers': ['console', 'log_file' 'mail_admins'],
            #'filters': ['special'],
            #'propagate': False,
            'propagate': True,
        },
    },
}

try:
    from local_etp_settings import *
except ImportError, exp:
    pass

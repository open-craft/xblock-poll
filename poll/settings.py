"""
Django settings for the xblock-poll project.
For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from __future__ import absolute_import
import os
import yaml

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# This is just a container for running tests, it's okay to allow it to be
# defaulted here if not present in environment settings
SECRET_KEY = os.environ.get('SECRET_KEY', '",cB3Jr.?xu[x_Ci]!%HP>#^AVmWi@r/W3u,w?pY+~J!R>;WN+,3}Sb{K=Jp~;&k')

# SECURITY WARNING: don't run with debug turned on in production!
# This is just a container for running tests
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'statici18n',
    'poll',
)

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'poll/translations'),
]

# statici18n
# http://django-statici18n.readthedocs.io/en/latest/settings.html

with open(os.path.join(BASE_DIR, 'poll/translations/config.yaml'), 'r') as locale_config_file:
    locale_config = yaml.load(locale_config_file, Loader=yaml.SafeLoader)

    LANGUAGES = [
        (code, code,)
        for code in locale_config['locales'] + locale_config['dummy_locales']
    ]

STATICI18N_DOMAIN = 'textjs'

# `PollI18N` might collide with other modules, using `PollXBlockI18N` to be more explicit
STATICI18N_NAMESPACE = 'PollXBlockI18N'
STATICI18N_PACKAGES = (
    'poll',
)
STATICI18N_ROOT = 'poll/public/js'
STATICI18N_OUTPUT_DIR = 'translations'

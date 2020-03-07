# This is a fairly standard Django settings file, with some special additions
# that allow addon applications to auto-configure themselves. If it looks 
# unfamiliar, please see our documentation:
#
#   http://docs.divio.com/en/latest/reference/configuration-settings-file.html
#
# and comments below.


# INSTALLED_ADDONS is a list of self-configuring Divio Cloud addons - see the
# Addons view in your project's dashboard. See also the addons directory in 
# this project, and the INSTALLED_ADDONS section in requirements.in.

INSTALLED_ADDONS = [
    # Important: Items listed inside the next block are auto-generated.
    # Manual changes will be overwritten.

    # <INSTALLED_ADDONS>  # Warning: text inside the INSTALLED_ADDONS tags is auto-generated. Manual changes will be overwritten.
    'aldryn-addons',
    'aldryn-django',
    'aldryn-sso',
    # </INSTALLED_ADDONS>
]

# Now we will load auto-configured settings for addons. See:
#
#   http://docs.divio.com/en/latest/reference/configuration-aldryn-config.html
#
# for information about how this works.
#
# Note that any settings you provide before the next two lines are liable to be
# overwritten, so they should be placed *after* this section.
import os
import sys
import datetime
from private import EMAIL_CONFIG, PRIVATE_QINIU_ACCESS_KEY, PRIVATE_QINIU_SECRET_KEY, \
    PRIVATE_QINIU_BUCKET_DOMAIN, PRIVATE_QINIU_BUCKET_NAME, PRIVATE_MEDIA_URL_PREFIX, PRIVATE_SITE_BASE_URL

import aldryn_addons.settings
aldryn_addons.settings.load(locals())

# Your own Django settings can be applied from here on. Key settings like
# INSTALLED_APPS, MIDDLEWARE and TEMPLATES are provided in the Aldryn Django
# addon. See:
#
#   http://docs.divio.com/en/latest/how-to/configure-settings.html
#
# for guidance on managing these settings.

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'post_apps'))
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'apps'))
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'extra_apps'))
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'auth'))


ARTICLE_PAGINATE_BY = 8
LANGUAGE_CODE = "en-us"
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

BOOK_MOVIE_PAGINATE_BY = 8

HAYSTACK_SEARCH_RESULTS_PER_PAGE = 7
INSTALLED_APPS.extend([
    # Extend the INSTALLED_APPS setting by listing additional applications here
    'corsheaders',
    
    'xadmin',

    'taggit',

    'rest_framework',
    
    'rest_auth',

    'rest_auth.registration',
    'rest_framework_swagger',
    'products',
    
    'orders',
    'django_filters',
    
    'crispy_forms',

    'twilio',
    'raven.contrib.django.raven_compat',
    'user_operation',
    
    'haystack',
    'base.apps.BaseConfig',
    'index',
    'material.apps.MaterialConfig',
    'movie.apps.MovieConfig',
    'album.apps.AlbumConfig',
    'post.apps.PostConfig',
    'comment.apps.CommentConfig',
    'user.apps.UserConfig',
    'post_user_operation.apps.PostUserOperationConfig',
    'book.apps.BookConfig'

])
SITE_ID = 1

TAGGIT_CASE_INSENSITIVE = True

CORS_ORIGIN_ALLOW_ALL = True

# authentication related stuff
AUTH_USER_MODEL = 'user.UserProfile'
APIKEY = 'd6c4ddbf50ab36611d2f52041a0b949e'
AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    'social_core.backends.weibo.WeiboOAuth2',
    'social_core.backends.qq.QQOAuth2',
    'social_core.backends.weixin.WeixinOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)
REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"

HAYSTACK_CONNECTIONS = {
    'default': {
        # For Whoosh:
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'),
        'INCLUDE_SPELLING': True,
    }
}
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=3600),
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
}
REST_FRAMEWORK_EXTENSIONS = {
    'DEFAULT_CACHE_RESPONSE_TIMEOUT': 60 * 15
}
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        # 'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day'
    },
    'NON_FIELD_ERRORS_KEY': 'error',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20,
}
private_key_path = os.path.join(BASE_DIR, 'apps/orders/keys/private_2048.txt')
ali_pub_key_path = os.path.join(BASE_DIR, 'apps/orders/keys/alipay_key_2048.txt')

# 第三方登录相关
SOCIAL_AUTH_WEIBO_KEY = 'foobar'
SOCIAL_AUTH_WEIBO_SECRET = 'bazqux'

SOCIAL_AUTH_QQ_KEY = 'foobar'
SOCIAL_AUTH_QQ_SECRET = 'bazqux'

SOCIAL_AUTH_WEIXIN_KEY = 'foobar'
SOCIAL_AUTH_WEIXIN_SECRET = 'bazqux'



CORS_ORIGIN_WHITELIST = [
    'http://localhost:3000',
    'http://localhost:8000',
    'http://localhost:8080',
]

RAVEN_CONFIG = {
    'dsn': 'https://<key>:<secret>@sentry.io/<project>',
}


TWILIO_SID = "AC5710ac7d9bfac0b9b6579cfc45c4db05"
TWILIO_TOKEN = "7a561a6601b5680bd47f8dd99030e912"
TWILIO_PHONE = "+12058138246"

MEDIA_URL_PREFIX = PRIVATE_MEDIA_URL_PREFIX
SITE_BASE_URL = PRIVATE_SITE_BASE_URL


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = EMAIL_CONFIG['EMAIL_HOST']
EMAIL_PORT = EMAIL_CONFIG['EMAIL_PORT']
EMAIL_HOST_USER = EMAIL_CONFIG['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = EMAIL_CONFIG['EMAIL_HOST_PASSWORD']
# EMAIL_USE_SSL = EMAIL_CONFIG['EMAIL_USE_SSL']
EMAIL_FROM = EMAIL_CONFIG['EMAIL_FROM']

REST_USE_JWT = True
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
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        # 'django.db.backends': {
        #     'handlers': ['console'],
        #     'level': 'DEBUG',
        # }
    }
}
# To see the settings that have been applied, use the Django diffsettings 
# management command. 
# See https://docs.divio.com/en/latest/how-to/configure-settings.html#list# todo: use mailgun

STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", "somekey")
STRIPE_PUBLISHABLE_KEY = os.environ.get("STRIPE_PUBLISHABLE_KEY", "publishkey")


# Douban Api
DOUBAN_API_URL = 'https://api.douban.com/v2'
# To see the settings that have been applied, use the Django diffsettings 
# management command. 
# See https://docs.divio.com/en/latest/how-to/configure-settings.html#list

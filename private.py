EMAIL_CONFIG = {
    'EMAIL_HOST': "", # mail server address
    'EMAIL_PORT': 25, # mail server port, usually 25
    'EMAIL_HOST_USER': "", # mail server account
    'EMAIL_HOST_PASSWORD': "", # mail server password
    'EMAIL_USE_TLS': False, # Whether to use TLS encryption connection, generally not used
    'EMAIL_FROM': "" # This item is generally the same as EMAIL_HOST
}

# Qiniu Yun related configuration
PRIVATE_QINIU_ACCESS_KEY = '' # Qiniu Access key
PRIVATE_QINIU_SECRET_KEY = '' # Qiniu Secret key
PRIVATE_QINIU_BUCKET_DOMAIN = '' # Qiniu Bucket domain
PRIVATE_QINIU_BUCKET_NAME = '' # Qiniu name

PRIVATE_MEDIA_URL_PREFIX = '' # Resource prefix used when accessing Cattle Cloud
PRIVATE_SITE_BASE_URL = '' # Site URL, for example as you site access domain
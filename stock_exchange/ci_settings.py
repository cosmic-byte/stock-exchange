from stock_exchange.settings import *  # pylint: disable=unused-wildcard-import

SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY", "alq7#8r33k!cv47r8pelqldnkl46v!b4-sfwvdo$x(=p%1read"
)
local_test_db = {"ENGINE": "django.db.backends.sqlite3", "NAME": "test_db"}

DATABASES = {
    "default": local_test_db
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'my_cache_table',
    }
}

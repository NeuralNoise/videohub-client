import os

DEBUG = True

DATABASES = {
    "default": {
        "NAME": "videohub-client",
        "ENGINE": "django.db.backends.sqlite3"
    }
}

INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    # third parties
    'djes',
    "djbetty",
    # me
    "videohub_client",
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
),

SECRET_KEY = "trustno1"

ES_CONNECTIONS = {
    "default": {
        "hosts": [os.environ.get('ELASTICSEARCH_HOST', 'localhost')]
    }
}

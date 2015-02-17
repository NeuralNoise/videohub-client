DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3"
    }
}

INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    # third parties
    "djbetty",
    "videohub_client",
)

MIDDLEWARE_CLASSES=(
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
),

SECRET_KEY = "trustno1"

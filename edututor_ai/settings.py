from pathlib import Path
import os
from datetime import timedelta

try:
    from dotenv import load_dotenv
except Exception:  # pragma: no cover
    load_dotenv = None

if load_dotenv:
    load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "change-me-in-production-secure-random-key-123456789")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Configuration des hÃ´tes autorisÃ©s pour Render
# Build ALLOWED_HOSTS as a flat list. environment variables may
# contain a comma-separated string and/or an explicit render hostname.
ALLOWED_HOSTS = []

# add explicit hosts from ALLOWED_HOSTS env var
raw = os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost")
for h in raw.split(","):
    if h:
        ALLOWED_HOSTS.append(h)

# render hostname (empty string if not set)
render_host = os.getenv("RENDER_EXTERNAL_HOSTNAME", "")
if render_host:
    ALLOWED_HOSTS.append(render_host)

# filter out any accidental empties
ALLOWED_HOSTS = [host for host in ALLOWED_HOSTS if host]

# Configuration de la base de donnÃ©es
if os.getenv('PYTHONANYWHERE'):
    # Configuration pour PythonAnywhere (MySQL)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('DATABASE_NAME', 'votre-username$db'),
            'USER': os.getenv('DATABASE_USER', 'votre-username'),
            'PASSWORD': os.getenv('DATABASE_PASSWORD', ''),
            'HOST': os.getenv('DATABASE_HOST', 'mysql.server'),
            'PORT': os.getenv('DATABASE_PORT', '3306'),
            'OPTIONS': {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            },
        }
    }
else:
    # Configuration pour dÃ©veloppement/local (PostgreSQL)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('PGDATABASE', 'edututor_db'),
            'USER': os.getenv('PGUSER', 'edututor'),
            'PASSWORD': os.getenv('PGPASSWORD', 'password'),
            'HOST': os.getenv('PGHOST', 'localhost'),
            'PORT': os.getenv('PGPORT', '5432'),
            'OPTIONS': {
                'sslmode': 'require' if os.getenv('RENDER') else 'disable',
            },
        }
    }

# Configuration Redis (optionnel)
REDIS_URL = os.getenv('REDIS_URL')

if REDIS_URL and not os.getenv('PYTHONANYWHERE'):
    # Redis disponible (Render, local, etc.)
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": [REDIS_URL],
            },
        },
    }
else:
    # Fallback vers InMemoryChannelLayer (PythonAnywhere, dÃ©veloppement)
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels.layers.InMemoryChannelLayer",
        },
    }

# Security settings
# In local dev, HTTPS is usually terminated elsewhere (or not used), so default to False.
_secure_default = "False" if DEBUG else "True"
SECURE_SSL_REDIRECT = os.getenv("SECURE_SSL_REDIRECT", _secure_default).lower() == "true"
SECURE_HSTS_SECONDS = int(os.getenv("SECURE_HSTS_SECONDS", "0" if DEBUG else "31536000"))
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", _secure_default).lower() == "true"
CSRF_COOKIE_SECURE = os.getenv("CSRF_COOKIE_SECURE", _secure_default).lower() == "true"
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "channels",
    "rest_framework",
    "rest_framework_simplejwt",
    "accounts",
    "chat",
    "documents",
    "subscriptions",
    "ai_services",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Pour servir les fichiers statiques
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "subscriptions.middleware.ProFeatureMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "edututor_ai.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "edututor_ai.wsgi.application"
ASGI_APPLICATION = "edututor_ai.asgi.application"

# SQLite only (MVP requirement)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "accounts.User"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "AUTH_HEADER_TYPES": ("Bearer",),
}

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# Gemini AI Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

FREE_DAILY_MESSAGE_LIMIT = int(os.getenv("FREE_DAILY_MESSAGE_LIMIT", "25"))
MAX_UPLOAD_SIZE_MB = int(os.getenv("MAX_UPLOAD_SIZE_MB", "10"))
MESSAGE_PAGE_SIZE = int(os.getenv("MESSAGE_PAGE_SIZE", "20"))
LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/dashboard/"


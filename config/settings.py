"""
Django settings for config project.
"""

import os
from pathlib import Path
from urllib.parse import urlparse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# Helper functions
def _split_env_list(value):
    return [item.strip() for item in value.split(",") if item.strip()]

def _load_dotenv(path):
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        key = key.strip()
        value = value.strip().strip("'\"")
        if key and key not in os.environ:
            os.environ[key] = value

_load_dotenv(BASE_DIR / ".env")

# Custom user model
AUTH_USER_MODEL = 'accounts.User'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-change-me-in-production")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "True").lower() in {"1", "true", "yes", "on"}

# Environment
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

# Allowed Hosts
if ENVIRONMENT == 'production':
    ALLOWED_HOSTS = ['*']  # Override in production with specific domains
else:
    DEFAULT_ALLOWED_HOSTS = "127.0.0.1,localhost,testserver,.ngrok-free.app,.ngrok-free.dev,.ngrok.io,.ngrok.app"
    ALLOWED_HOSTS = _split_env_list(os.getenv("ALLOWED_HOSTS", DEFAULT_ALLOWED_HOSTS))

# CSRF Trusted Origins
if ENVIRONMENT == 'production':
    CSRF_TRUSTED_ORIGINS = ['https://*.railway.app', 'https://*.up.railway.app']
else:
    DEFAULT_CSRF_TRUSTED_ORIGINS = (
        "https://127.0.0.1,https://localhost,https://*.ngrok-free.app,"
        "https://*.ngrok-free.dev,https://*.ngrok.io,https://*.ngrok.app"
    )
    CSRF_TRUSTED_ORIGINS = _split_env_list(os.getenv("CSRF_TRUSTED_ORIGINS", DEFAULT_CSRF_TRUSTED_ORIGINS))

# Application definition
INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "accounts",
    "classes",
    "students",
    "subjects",
    "assessments",
    "reports",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # "config.middleware.SessionIdleTimeoutMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        'DIRS': [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "config.wsgi.application"

# Disable debug in production
DEBUG = False

# Use less memory-intensive session engine
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

# Reduce database connection pool
if 'DATABASE_URL' in os.environ:
    DATABASES['default']['CONN_MAX_AGE'] = 0  # type: ignore # Don't keep persistent connections
    DATABASES['default']['CONN_HEALTH_CHECKS'] = False # type: ignore

# Database configuration
import dj_database_url

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME', 'postgres'),
            'USER': os.getenv('DB_USER', 'postgres'),
            'PASSWORD': os.getenv('DB_PASSWORD', ''),
            'HOST': os.getenv('DB_HOST', 'localhost'),
            'PORT': os.getenv('DB_PORT', '5432'),
            'OPTIONS': {
                'sslmode': 'require',
            },
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Africa/Nairobi"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Authentication URLs
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "dashboard"
LOGOUT_REDIRECT_URL = "login"

# Security settings for production
if ENVIRONMENT == 'production' or not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = "DENY"
    SECURE_REFERRER_POLICY = "same-origin"
    SECURE_HSTS_SECONDS = int(os.getenv("SECURE_HSTS_SECONDS", "31536000"))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ========== SESSION SECURITY SETTINGS ==========
SESSION_COOKIE_AGE = 300  # 5 minutes
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_CLEAR_ON_LOGOUT = True

if ENVIRONMENT == 'production' or not DEBUG:
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = 'Strict'

# ========== JAZZMIN SETTINGS ==========
JAZZMIN_SETTINGS = {
    "site_title": "Ikonex Academy",
    "site_header": "Ikonex Academy",
    "welcome_sign": "Welcome to Ikonex Academy Management System",
    "copyright": "Ikonex Academy",
    "site_logo": "images/ikonex.png",
    "login_logo": "images/ikonex.png",
    "custom_css": None,
    "custom_js": None,
    "show_ui_builder": False,
    "show_navbar": True,
    "order_with_respect_to": [
        "accounts",
        "classes",
        "students",
        "subjects",
        "assessments",
        "reports",
    ],
    "icons": {
        "auth.User": "fas fa-users",
        "auth.Group": "fas fa-users-cog",
        "classes.ClassStream": "fas fa-building",
        "students.Student": "fas fa-user-graduate",
        "subjects.Subject": "fas fa-book",
        "subjects.ClassSubject": "fas fa-diagram-project",
        "assessments.Assessment": "fas fa-pencil-alt",
        "assessments.Score": "fas fa-chart-line",
        "assessments.GradeScale": "fas fa-percent",
        "reports.Report": "fas fa-file-alt",
    },
    "app_icons": {
        "accounts": "fas fa-user-shield",
        "classes": "fas fa-school",
        "students": "fas fa-users",
        "subjects": "fas fa-book-open",
        "assessments": "fas fa-tasks",
        "reports": "fas fa-chart-bar",
        "auth": "fas fa-lock",
    },
    "list_filter": ["sticky"],
    "search_model": ["auth.User", "students.Student", "classes.ClassStream"],
    "default_model": None,
    "show_sidebar": True,
    "navigation": [
        {
            "name": "Core Management",
            "icon": "fas fa-home",
            "models": [
                {"name": "Dashboard", "url": "/admin/", "icon": "fas fa-tachometer-alt"},
            ]
        },
        {
            "name": "Student Management",
            "icon": "fas fa-users",
            "models": [
                {"name": "Students", "url": "/admin/students/student/", "icon": "fas fa-user-graduate"},
                {"name": "Class Streams", "url": "/admin/classes/classstream/", "icon": "fas fa-building"},
            ]
        },
        {
            "name": "Academic",
            "icon": "fas fa-book",
            "models": [
                {"name": "Subjects", "url": "/admin/subjects/subject/", "icon": "fas fa-book"},
                {"name": "Class Subjects", "url": "/admin/subjects/classsubject/", "icon": "fas fa-diagram-project"},
            ]
        },
        {
            "name": "Assessment",
            "icon": "fas fa-tasks",
            "models": [
                {"name": "Assessments", "url": "/admin/assessments/assessment/", "icon": "fas fa-pencil-alt"},
                {"name": "Scores", "url": "/admin/assessments/score/", "icon": "fas fa-chart-line"},
                {"name": "Grade Scales", "url": "/admin/assessments/gradescale/", "icon": "fas fa-percent"},
            ]
        },
        {
            "name": "Reports",
            "icon": "fas fa-chart-bar",
            "models": [
                {"name": "Class Reports", "url": "/reports/", "icon": "fas fa-file-alt"},
                {"name": "Student Reports", "url": "/reports/students/", "icon": "fas fa-file-pdf"},
            ]
        },
        {
            "name": "Security",
            "icon": "fas fa-shield-alt",
            "models": [
                {"name": "Users", "url": "/admin/auth/user/", "icon": "fas fa-user"},
                {"name": "Groups", "url": "/admin/auth/group/", "icon": "fas fa-users-cog"},
            ]
        },
    ],
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-teal",
    "accent": "accent-teal",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-teal",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "default",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
    },
}


import subprocess
import sys

if os.environ.get('RAILWAY_ENVIRONMENT'):
    # Auto-collect static files on Railway
    subprocess.call([sys.executable, 'manage.py', 'collectstatic', '--noinput'])
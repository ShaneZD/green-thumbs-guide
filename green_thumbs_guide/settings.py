"""
Django settings for green_thumbs_guide project.
Generated by 'django-admin startproject' using Django 5.1.1.
For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
from pathlib import Path

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-kc4($3u&@&f%_3$7!u-&37i+qcar_3fe%tz*#_&q==%&4c*lzz'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Hosts/domain names that are valid for this site; required if DEBUG is False
ALLOWED_HOSTS = []

# API key for OpenWeatherMap to fetch weather data
OPENWEATHERMAP_API_KEY = 'a070d2f102c9476238c715131a9b58a5'

# Ensures URLs end with a slash
APPEND_SLASH = True

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'forum',  # Custom app for forum functionality
    'core',   # Custom app for core functionality
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URL configuration module
ROOT_URLCONF = 'green_thumbs_guide.urls'

# Base directory for the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Template settings
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI application path
WSGI_APPLICATION = 'green_thumbs_guide.wsgi.application'

# Database configuration using dj_database_url
BASE_DIR = Path(__file__).resolve().parent.parent

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'green_thumb_db',  # Your database name
        'USER': 'green_thumb_db_user',  # Your database username
        'PASSWORD': 'Xno6ElnSlcI8Byj7q2VMuhh31aSMBDbC',  # Your database password
        'HOST': 'dpg-cs6p7l23esus73b6o10g-a.frankfurt-postgres.render.com',  # Your database host
        'PORT': '5432',  # Port for PostgreSQL
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization settings
LANGUAGE_CODE = 'en-uk'
TIME_ZONE = 'GMT'
USE_I18N = True
USE_TZ = True

# Static files settings (CSS, JavaScript, Images)
STATIC_URL = '/static/'  
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
STATIC_ROOT = os.path.join(BASE_DIR, 'static') 

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Authentication and redirection settings
LOGIN_URL = '/registration/login/'
LOGIN_REDIRECT_URL = 'core:home'
LOGOUT_REDIRECT_URL = 'core:home'

# Media files settings
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

ALLOWED_HOSTS = ['green-thumbs-guide.onrender.com', 'localhost', '127.0.0.1']


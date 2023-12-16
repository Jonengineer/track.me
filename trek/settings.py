from pathlib import Path
import os


# -*- coding: utf-8 -*-

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-5xr1*i&&9h_@0ev6uxqs#!r!$76vmvxx0onyc(d^v=x5s#($o@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []



# Указываем путь к данным GDAL
GDAL_LIBRARY_PATH = r"C:\\Users\\Евгений\\AppData\\Local\\Programs\\Python\\Python311\\Lib\\site-packages\\osgeo\\gdal304.dll"

GEOS_LIBRARY_PATH = 'C:\\Users\\Евгений\\AppData\\Local\\Programs\\Python\\Python311\\Lib\\site-packages\\osgeo\\geos_c.dll'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'travel',
    'user',
    'django.contrib.gis',
    'material',
    'appbase'
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

ROOT_URLCONF = 'trek.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'user', 'templates'),
            os.path.join(BASE_DIR, 'travel', 'templates'),
            os.path.join(BASE_DIR, 'appbase', 'templates'),
        ],
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

WSGI_APPLICATION = 'trek.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'track',
        'USER': 'postgres',
        'PASSWORD': '7141',
        'HOST': 'localhost',
        'PORT': '5432',
        'OPTIONS': {
            'options': '-c search_path=public',
            'client_encoding': 'UTF8',  # Используйте 'client_encoding' вместо 'charset'
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [    
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'user.validators.CustomPasswordValidator',  # Заменяем нашим кастомным валидатором
        'OPTIONS': {
            'min_length': 8,
            'special_characters': ['@', '&', '$', '%', '!', '#', '*'],
        }
    },
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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'travel', 'media')

AUTH_USER_MODEL = 'user.User'

AUTHENTICATION_BACKENDS = [
    'user.authlogin.EmailLogin',  # Путь к вашему backend
    'django.contrib.auth.backends.ModelBackend',
]

CSRF_COOKIE_SECURE = True

LOGIN_URL = 'user:user_login'

LANGUAGE_CODE = 'ru-RU'

USE_I18N = True

USE_L10N = True
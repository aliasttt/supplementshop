
import os
import dj_database_url
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


AUTH_USER_MODEL = 'supplementapp.RegisterModel'


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '02a16fbd97299a5496800ddfddd0ba15a458386a18df3830629fee80469d6596023de3c0e79656797dbf8ce362a33208ba63'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'supplementapp',
    'rest_framework',
    'corsheaders',
    # برای این که فرانت‌اند بتواند به ای پی ای بک اند دسترسی داشته باشد با دوتا دامنه متفاوت
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware', 
    # for corsheaders
    'django.middleware.locale.LocaleMiddleware',      
    # برای افزودن زبان
]


# AUTHENTICATION_BACKENDS = [
#     'django.contrib.auth.backends.ModelBackend',  
# ]




CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000', 
    'http://localhost:8000',  
]

ROOT_URLCONF = 'supproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],  # اگر از دایرکتوری سفارشی برای قالب‌ها استفاده می‌کنید
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'supplementapp.context_processors.cart_items_count',  # کانتکست پروسسور شما
            ],
        },
    },
]


WSGI_APPLICATION = 'supproject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES ={

    "default" :dj_database_url.config(default = os.environ.get("DATABASE_URL"))
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),  # مسیر پوشه استاتیک پروژه شما
]
#وقتی تنظیمات استاتیک فایلو ست کنی مشکل فونت حل میشه


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



LANGUAGES = [
    ('en', 'English'),   
    ('tr', 'Turkish'),   
    ('fa', 'Farsi'),     
]

#  تنظیم زبان پیشفرض جالبیش اینه که پنل ادمین هم فارسی میشه
LANGUAGE_CODE = 'fa'


USE_I18N = True    #برای استفاده از بلاک ترنس و gettext
LOCALE_PATHS = [
    BASE_DIR / 'locale',  # مسیر فایل‌های ترجمه
]

#خب برای ایجاد ترجمه و اضافه کردن فایل های زبان مختلف باید محیط مجازی باشه حتما  و حتما باید از یوز ای 18 استفاده بشه مگرنه ارور گت تکست میده تاوقتی از ترنس استغفاده نکنی هیچموقع فایلایه داخل لوکال ساخته نمیشه یه فولدر خالی ایجاد میشه 


SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # استفاده از پایگاه داده برای ذخیره نشست‌ها
SESSION_COOKIE_AGE = 3600 





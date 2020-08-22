"""
Django settings for TestDog project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from datetime import timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6tclrlfu#n0pku7!ws@dpf_81o2$x6w&4zizae7cm^q(l8g2et'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'simpleui',
    'corsheaders',  # 跨域
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app.apps.AppConfig',
    'rest_framework',
    'djcelery',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'TestDog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'TestDog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'testdog',
        'USER': 'root',
        'PASSWORD': 'mld123456',
        'HOST': 'localhost',
        'PORT': '3306',

    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/ShangHai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, '/static/')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

# 媒体文件
MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, "static/media")
# 上传文件权限
FILE_UPLOAD_PERMISSIONS = 0o644

# 上传文件最大50M
FILE_UPLOAD_MAX_MEMORY_SIZE = 50 * 1024 * 1024

# log配置
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        # 打印终端
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },

        # debug日志处理器
        'default': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, "static/logs/debug.log"),
            'formatter': 'verbose',
            'encoding': 'utf-8'
        },
        # error日志处理器
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, "static/logs/error.log"),
            'maxBytes': 1024 * 1024 * 50,
            'formatter': 'verbose',
            'encoding': 'utf-8'
        }
    },
    'loggers': {
        'td_log': {
            'handlers': ['default', 'error', ],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# admin
# SIMPLEUI_LOGO = 'https://avatars2.githubusercontent.com/u/13655483?s=60&v=4'
# SIMPLEUI_INDEX = 'http://admin.mayansen.cn'
SIMPLEUI_HOME_INFO = False
SIMPLEUI_HOME_ACTION = True
# SIMPLEUI_DEFAULT_ICON = False

# SIMPLEUI_DEFAULT_THEME = 'x-red.css'



# 跨域
#  新增以下配置  #
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
# Origin '*' in CORS_ORIGIN_WHITELIST is missing scheme 出现该错误则将其注释掉
# CORS_ORIGIN_WHITELIST = (
#   "*"
# )
CORS_ALLOW_METHODS = (
  'DELETE',
  'GET',
  'OPTIONS',
  'PATCH',
  'POST',
  'PUT',
  'VIEW',
)
CORS_ALLOW_HEADERS = (
  'XMLHttpRequest',
  'X_FILENAME',
  'accept-encoding',
  'authorization',
  'content-type',
  'dnt',
  'origin',
  'user-agent',
  'x-csrftoken',
  'x-requested-with',
  'Pragma',
)






# # redis配置celery
import djcelery
djcelery.setup_loader()
# # redis链接串
# # "redis://:密码@主机ip:端口/库序号"
BROKER_URL = "redis://127.0.0.1:6379/7"
# # 注册任务文件
CELERY_IMPORTS = ("app.task")
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'  # 定时任务
# 下面是定时任务的设置，一共配置了三个定时任务.
from celery.schedules import crontab
CELERYBEAT_SCHEDULE = {
#     # 定时任务一：　每24小时周期执行任务(del_redis_data)
    'seconds-12': {
        "task": "app.task.lottery",  # 定时执行的任务的函数名称
#         # "schedule": crontab(hour='*/24'),
#         "schedule": timedelta(seconds=60 * 5),  # 定时执行的间隔时间
#         "args": (),  # 定时任务传参
    },
#     # 定时任务二:　每天的凌晨12:30分，执行任务(back_up1)
#     #     u'生成日报表': {
#     #         'task': 'Ai_ke.task.userdayusdt',
#     #         'schedule': crontab(minute=30, hour=0),
#     #         "args": ()
#     #     },
}
CELERYD_MAX_TASKS_PER_CHILD = 2



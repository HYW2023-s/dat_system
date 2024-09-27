"""
Django settings for dat project.

Generated by 'django-admin startproject' using Django 4.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-4-1d^1!_v*mdt=8yu7w8a)+qlsnxc+%_f^-k9b_uc*q-%36o1e"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
# SECURE_SSL_REDIRECT = True

# Application definition

INSTALLED_APPS = [
    # ui
    "simpleui",
    'widget_tweaks',
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # 应用
    "dat_app.apps.DatAppConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    # "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # 权限校验中间件
    "dat_app.middleware.auth.M1",
    # 动态菜单中间件
    "dat_app.middleware.dynamic_menu.M2",
]

ROOT_URLCONF = "dat.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates']
        ,
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "dat.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',  # 默认
#         'NAME': '',  # 连接的数据库
#         'HOST': '',  # mysql的ip地址
#         'PORT': ,  # mysql的端口
#         'USER': '',  # mysql的用户名
#         'PASSWORD': ''  # mysql的密码
#     }

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "zh-hans"

TIME_ZONE = "Asia/Shanghai"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# django simpleui设置

# 去掉默认Logo或换成自己Logo链接
# SIMPLEUI_LOGO = ""

# 关闭原先首页广告
SIMPLEUI_HOME_INFO = False
SIMPLEUI_ANALYSIS = False

# 关闭最近动作
SIMPLEUI_HOME_ACTION = False

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# 动态路由配置
SIMPLEUI_HOME_TITLE = '任务介绍'  # 首页标题
SIMPLEUI_CONFIG = {
    'system_keep': True,
    'menu_display': ['任务列表'],
    'dynamic': True,
    'menus': [
        {
            'app': 'auth',
            'name': '用户管理',
            'icon': 'fa-solid fa-user',
            'models': [
                {
                    'name': '用户',
                    'url': 'auth/user',
                    'icon': 'fa-regular fa-user-pen',
                },
                {
                    'name': '组',
                    'url': 'auth/group',
                    'icon': 'fa-solid fa-user-group',
                },
            ]
        },
        {
            'name': '任务列表',
            'icon': 'fa fa-th-list',
            'models': [
                {
                    'name': '任务介绍',
                    'url': '/introduction',
                    'icon': 'fa-solid fa-file-invoice',
                },
                {
                    'name': '开始测试',
                    'url': '/index',
                    'icon': 'fa-regular fa-hourglass-start',
                },
                {
                    'name': '结果查询',
                    'url': '/results',
                    'icon': 'fa-regular fa-square-poll-vertical',
                },
            ],
        },
        {
            'name': "数据分析",
            'icon': 'fa-regular fa-square-poll-vertical',
            'models': [
                {
                    'name': '分析视图',
                    'url': '/dataAnalysis',
                    'icon': 'fa-regular fa-square-poll-vertical',
                },
                {
                    'name': "任务管理",
                    'url': '/updatelimited',
                    'icon': 'fa fa-th-list',
                },
                {
                    'name': "用户上传",
                    'url': '/uploaduser',
                    'icon': 'fa-solid fa-user-group',
                },
            ],
        },
    ]
}
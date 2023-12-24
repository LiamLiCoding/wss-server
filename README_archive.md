![license](https://img.shields.io/github/license/Haozheng-Li/wss-client)

# wss-server

Based on Django, wss-server is high performance web and IOT server. 

## Features

1. Provide Websocket long-live API and Restful HTTP API for data communication with client.
2. Beautiful and responsive front-end page.
3. Web page real-time notification.
4. Complete user accounts system.
5. User authentication management (developing)
6. Device management and performance monitoring.
7. Data analysis and visualization.
8. SMS alert and email alert.

## Preview

![dashboard](https://github.com/Haozheng-Li/wss-server/assets/47854126/dc34b21f-d46a-4501-8afe-028e65be2c40)

![device_details](https://github.com/Haozheng-Li/wss-server/assets/47854126/57a68a57-ddba-4064-b188-ac79763dcb25)

## Requirements

- Python 3.6+
- Django 4.0+

## Installation

1. Install nesserary package

```
pip install -r requirements.txt
```

2. Project Configure

Create a configure file named `key_define.py` to `wss-server/wss_server`.
Fill the basic config:

```Python
DJANGO_SECRET_KEY = 'your_django_secret_ket'

DATABASE_INFO = {
    'default': {
      your_django_database_settings
    }
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": ["redis://:your_redis_url"],
        },
    },
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://your_redis_url",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": "your_password"
        }
    }
}

# Optional config

# Github application settings, for accounts login
GITHUB_CLIENT_ID = 'your_github_client_id'
GITHUB_CLIENT_SECRET = 'your_github_client_secret'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = ''
EMAIL_PORT = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_SUBJECT_PREFIX = ''
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
ADMINS = ()


```

4. Run project locally

```
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

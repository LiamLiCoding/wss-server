![license](https://img.shields.io/github/license/Haozheng-Li/wss-client)

# wss-server

Based on Django, wss-server is high performance web and IOT server. 

Website: [WSS-Web](https://wssweb.net/)

## Features

1. Provide Websocket long-live API and Restful HTTP API for data communication with client.
2. Beautiful and responsive front-end page.
3. Web page real-time notification.
4. Complete user accounts system.
5. User authentication management (developing)
6. Device management and performance monitoring.
7. Data analysis and visulization.
8. SMS alert and email alert.

## Preview

<img width="1440" alt="device_list" src="https://user-images.githubusercontent.com/47854126/225729290-502c222b-ee2b-4110-8275-37fb6fe5330d.png">

<img width="1440" alt="device_detail_online" src="https://user-images.githubusercontent.com/47854126/225729313-f0fa58d8-6366-4d95-a914-00a8c588f4f0.png">

## Client

It is recommended to use it with [wss-client](https://github.com/Haozheng-Li/wss-client). 

wss-client is an IoT endpoint client written in Python. It has functions such as terminal device operation performance monitoring, camera image recognition, and intrusion behavior detection. With wss-client, it can communicate with wss-server through websocket protocol to realize data mutual transmission.

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

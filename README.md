# drf-example

> Library reference
>
> [Etuloser/e-dockerfile: Store my dockerfile (github.com)](https://github.com/Etuloser/e-dockerfile)
>
> [Etuloser/drf-example (github.com)](https://github.com/Etuloser/drf-example)

## 项目构建

### 初始化项目

```bash

cd /srv
mkdir drf-example
cd drf-example
django-admin startproject demo .  # note .
cd demo
django-admin startapp app
cd ..
python3 manage.py migrate
python3 manage.py createsuperuser --email admin@example.com --username admin

pip install django-simpleui
```

*demo.settings*
```python
ALLOWED_HOSTS = ['*']

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

STATIC_ROOT = os.path.join(BASE_DIR, "static")

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}
```

### NGINX配置

这里使用NGINX容器，YAML文件链接：

*[e-dockerfile/docker-compose.yml at master · Etuloser/e-dockerfile (github.com)](https://github.com/Etuloser/e-dockerfile/blob/master/nginx-alpine/docker-compose.yml)*

nginx配置文件链接：

*[e-dockerfile/default.conf at master · Etuloser/e-dockerfile (github.com)](https://github.com/Etuloser/e-dockerfile/blob/master/nginx-alpine/default.conf)*

关键配置如下：

```nginx
upstream django {
    server unix:///srv/drf-example/demo/demo.sock; # for a file socket
    # server 0.0.0.0:30000; # for a web port socket (we'll use this first)
}

server {
    listen       80;
    ...
    # Django app
    location / {
        uwsgi_pass  django;
        include     /etc/nginx/uwsgi_params; # the uwsgi_params file you installed
    }
    ...
}
```

### uWSGI配置

```bash
pip install uwsgi
```

配置文件链接：

*[drf-example/uwsgi.ini at main · Etuloser/drf-example (github.com)](https://github.com/Etuloser/drf-example/blob/main/demo/uwsgi.ini)*

关键配置如下：

```ini
[uwsgi]
; socket = 0.0.0.0:30000
socket = /srv/drf-example/demo/demo.sock
chdir = /srv/drf-example
; wsgi-file = demo/wsgi.py
module = demo.wsgi
master = true
; env = DJANGO_SETTINGS_MODULE=demo.settings
processes = 4
chmod-socket = 666
; threads = 2
; stats = 0.0.0.0:30001
```


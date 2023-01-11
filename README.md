# drf-example

> Library reference
>
> [Setting up Django and your web server with uWSGI and nginx — uWSGI 2.0 documentation (uwsgi-docs.readthedocs.io)](https://uwsgi-docs.readthedocs.io/en/latest/tutorials/Django_and_nginx.html)
>
> [First steps with Django — Celery 5.2.7 documentation (celeryq.dev)](https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html)
>
> [celery/examples/django at master · celery/celery (github.com)](https://github.com/celery/celery/tree/master/examples/django/)
>
> [Etuloser/e-dockerfile: Store my dockerfile (github.com)](https://github.com/Etuloser/e-dockerfile)
>
> [Etuloser/drf-example (github.com)](https://github.com/Etuloser/drf-example)

## 项目构建

### 初始化项目

```bash
cd /srv
mkdir dr
cd drf
django-admin startproject server .  # note .
cd server
django-admin startapp core
cd ..
python3 manage.py migrate
python3 manage.py createsuperuser --email admin@example.com --username admin

python3 manage.py collectstatic
```

*services.settings*
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

*services.app.serializers*

```python
from django.contrib.auth.models import User, Group
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
```

*services.app.views*

```python
from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets
from .serializers import GroupSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

```

*services.urls*

```python
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from services.app import views as app_views

router = routers.DefaultRouter()
router.register(r'users', app_views.UserViewSet)
router.register(r'groups', app_views.GroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
]

```

### NGINX配置

这里使用NGINX容器，YAML文件链接：

*[e-dockerfile/docker-compose.yml at master · Etuloser/e-dockerfile (github.com)](https://github.com/Etuloser/e-dockerfile/blob/master/nginx-alpine/docker-compose.yml)*

nginx配置文件链接：

*[e-dockerfile/default.conf at master · Etuloser/e-dockerfile (github.com)](https://github.com/Etuloser/e-dockerfile/blob/master/nginx-alpine/default.conf)*

关键配置如下：

```nginx
upstream django {
    server unix:///srv/drf-example/services.sock; # for a file socket
    # server 0.0.0.0:30000; # for a web port socket (we'll use this first)
}

server {
    listen       80;
    ...
    location /static {
        alias /srv/drf-example/static; # your Django project's static files - amend as required
    }
    
    # Finally, send all non-media requests to the Django server.
    location / {
        uwsgi_pass  django;
        include     /etc/nginx/uwsgi_params; # the uwsgi_params file you installed
    }
    ...
}
```

### uWSGI配置

```bash
# 安装
pip install uwsgi
```

配置文件链接：

*[drf-example/uwsgi.ini at main · Etuloser/drf-example (github.com)](https://github.com/Etuloser/drf-example/blob/main/uwsgi.ini)*

关键配置如下：

```ini
[uwsgi]
socket = /srv/drf-example/services.sock
chdir = /srv/drf-example
module = services.wsgi
master = true
processes = 4
chmod-socket = 666
```

### supervisord配置

```bash
# 安装
pip install supervisord
# 初始化配置文件
echo_supervisord_conf > /etc/supervisor/supervisord.conf
```

*/etc/supervisor/supervisord.conf*

关键配置如下

```ini
...
[inet_http_server]          ; inet (TCP) server disabled by default
port=*:30091                 ; ip_address:port specifier, *:port for all iface
username=admin               ; default is no username (open server)
password=youpass
...
[include]
files = /srv/drf-example/supervisord.ini
```

*/srv/drf-example/supervisord.ini*

```ini
[program:drf-example]
command = uwsgi --ini uwsgi.ini
directory=/srv/drf-example
stdout_logfile=/srv/drf-example/logs/stdout.log
autostart=true
autorestart=true
user=root
startsecs=3
# 启动优先级
priority=998

[program:drf-example-celery]
command = celery -A services worker -l INFO
directory=/srv/drf-example
stdout_logfile=/srv/drf-example/logs/celery.log
autostart=true
autorestart=true
user=root
startsecs=3
priority=999

[program:drf-example-flower]
command = celery -A services flower --port=30555
directory=/srv/drf-example
stdout_logfile=/srv/drf-example/logs/flower.log
autostart=true
autorestart=true
user=root
startsecs=3
priority=997
```

### rabbitmq配置

这里使用rabbitmq容器，YAML文件链接：

*[e-dockerfile/docker-compose.yml at master · Etuloser/e-dockerfile (github.com)](https://github.com/Etuloser/e-dockerfile/blob/master/rabbitmq/docker-compose.yml)*

因为部署的是带插件的版本，可以访问http://ip:15672进入管理界面

![image-20220816213311910](D:\develop\OneDrive\图片\文章截图\image-20220816213311910.png)

进入容器配置一下rabbitmq

```bash
rabbitmqctl add_user myuser mypassword
rabbitmqctl add_vhost myvhost
rabbitmqctl set_user_tags myuser mytag
rabbitmqctl set_permissions -p myvhost myuser ".*" ".*" ".*"
```

### celery配置

```bash
# 安装celery和flower(监控)
pip install celery flower
```

*services.celery*

```python
import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'services.settings')

app = Celery('services')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
```

*services.settings*

```python
# celery settings
CELERY_BROKER_URL = 'amqp://myuser:mypassword@119.91.25.133:30567/myvhost'

#: Only add pickle to this list if your broker is secured
#: from unwanted access (see userguide/security.html)
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_BACKEND = 'rpc://myuser:mypassword@119.91.25.133:30567/myvhost'
CELERY_TASK_SERIALIZER = 'json'
```

同样，flower的web界面地址为http://ip:30555

![image-20220816215547875](D:\develop\OneDrive\图片\文章截图\image-20220816215547875.png)

可以看到已经读到celery了

测试调用一下task

```python
$ python ./manage.py shell
>>> from servicesapp.tasks import add, mul, xsum
>>> res = add.delay(2,3)
>>> res.get()
5
```


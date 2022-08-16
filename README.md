# drf-example

> Library reference
>
> [Etuloser/e-dockerfile: Store my dockerfile (github.com)](https://github.com/Etuloser/e-dockerfile)
>
> 

```bash
cd /srv
mkdir drf-example
cd drf-example
django-admin startproject demo .  # note .
```

[e-dockerfile/default.conf at master · Etuloser/e-dockerfile (github.com)](https://github.com/Etuloser/e-dockerfile/blob/master/nginx-alpine/default.conf)

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


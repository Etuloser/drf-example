FROM python:latest

WORKDIR /srv/edrf

COPY requirements.txt ./

RUN pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . .

CMD [ "uwsgi", "--ini", "uwsgi.ini"]

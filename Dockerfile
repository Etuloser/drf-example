FROM python:latest

WORKDIR /srv/drf-example

COPY requirements.txt ./

RUN pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . .

CMD [ "python", "manage.py", "run", "dev"]

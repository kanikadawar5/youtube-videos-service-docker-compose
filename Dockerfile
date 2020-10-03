FROM python:3.7.3-stretch

WORKDIR /project
ADD . /project

COPY requirements.txt /tmp/

RUN pip install -r /tmp/requirements.txt

CMD [ "python3", "app.py" ]
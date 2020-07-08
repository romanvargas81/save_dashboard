FROM python:3.7.7-stretch

ADD requirements.txt /srv/build/requirements.txt
RUN pip3 install -r /srv/build/requirements.txt

COPY ./uwsgi.ini /srv/uwsgi.ini
COPY ./app /srv/app

WORKDIR /srv

VOLUME ["/var/run/uwsgi"]
CMD ["uwsgi", "--ini", "/srv/uwsgi.ini"]
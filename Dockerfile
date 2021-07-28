FROM python:3

EXPOSE 8888


WORKDIR /usr/src/app

COPY . .


CMD fcgi-pm.py

ENTRYPOINT [ "python3" ]

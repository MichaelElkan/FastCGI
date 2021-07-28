# getting base image ubuntu
FROM python:3

EXPOSE 8888

ARG executable
ARG count
ARG socket
ARG queue-size

WORKDIR /usr/src/app

COPY . .


#RUN apt-get update && apt-get install -y python3

CMD fcgi-pm.py --socket=${socket} --count=${count} --queue-size=${queue-size} --executable=${executable}

ENTRYPOINT [ "python3" ]

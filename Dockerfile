# getting base image ubuntu
FROM ubuntu

EXPOSE 8888

ARG executable
ARG count
ARG socket
ARG queue-size

RUN apt-get update && apt-get install -y python3

CMD python3 fcgi-pm.py --socket=${socket} --count=${count} --queue-size=${queue-size} --executable=${executable}


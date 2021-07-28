# getting base image ubuntu
FROM ubuntu

EXPOSE 8888

ARG executable
ARG count
ARG socket
ARG queue-size

CMD python3 fcgi-pm.py --socket=${socket} --count=${count} --queue-size=${queue-size} --executable=${executable}


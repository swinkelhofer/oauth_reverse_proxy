FROM alpine
ADD / /opt
RUN apk update
RUN apk add --no-cache --update python python-dev py-pip g++ libffi-dev py-crypto openssl-dev git py-gunicorn
# RUN cd /opt/ && git submodule init && git submodule update
RUN ls -la /opt/oauth/
RUN pip install -r /opt/requirements.txt
RUN apk del g++ git python-dev
EXPOSE 80
WORKDIR /opt
CMD gunicorn -w 10 -b 0.0.0.0:5000 main:app

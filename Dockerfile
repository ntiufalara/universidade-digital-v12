FROM ubuntu:16.04

RUN \
  apt-get update && \
  apt-get install -y python3-pip python3-dev libxml2-dev libxslt1-dev libevent1-dev libsasl2-dev libldap2-dev nano wkhtmltopdf

RUN apt-get install npm wget -y && npm install -g less n && n lts

# Set the locale
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y locales

RUN sed -i -e 's/# pt_BR.UTF-8 UTF-8/pt_BR.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=pt_BR.UTF-8

ENV LANG pt_BR.UTF-8

# Code config
WORKDIR /src
ADD . /src
RUN pip3 install -r requirements.txt

# Entry-point
CMD ["/bin/bash", "/src/start_server.sh"]

#!/usr/bin/env bash

sudo apt-get install postgresql-server-dev-all build-essential python3-dev python2.7-dev libldap2-dev libsasl2-dev \
			slapd ldap-utils python-tox lcov valgrind postgresql python3-ldap python3-psutil

pip3 install -r requirements.txt



#!/usr/bin/env bash

sudo apt-get install postgresql-server-dev-11 build-essential python3-dev python2.7-dev libldap2-dev libsasl2-dev \
			slapd ldap-utils python-tox lcov valgrind postgresql python3-ldap

pip3 install -r requirements.txt



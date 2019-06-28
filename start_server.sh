#!/usr/bin/env bash

pip3 install -r requirements.txt
/usr/bin/python3 /src/odoo-bin -u all -d ud -r odoo -w odoo --db_host=127.0.0.1

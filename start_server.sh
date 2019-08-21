#!/usr/bin/env bash

ODOO_ENV=${ODOO_ENV:='prod'}

pip3 install -r requirements.txt

if [[ ${ODOO_ENV} == 'dev' ]]; then
  /usr/bin/python3 /src/odoo-bin -u all -d odoo -r odoo -w odoo --db_host=127.0.0.1 --dev=all
elif [[ ${ODOO_ENV} == 'prod' ]]; then
  /usr/bin/python3 /src/odoo-bin -u all -d ud -r odoo -w odoo --db_host=127.0.0.1 --logfile=/src/access.log --logrotate
fi

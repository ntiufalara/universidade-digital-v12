#!/usr/bin/env bash

ODOO_ENV=${ODOO_ENV:='prod'}

pip3 install -r requirements.txt

if [[ ${ODOO_ENV} == 'dev' ]]; then
  /usr/bin/python3 /src/odoo-bin -u all -d odoo --db_port=5433 -r odoo -w odoo --db_host=127.0.0.1 --dev=all --no-database-list
elif [[ ${ODOO_ENV} == 'prod' ]]; then
  /usr/bin/python3 /src/odoo-bin -u all -d ud --db_port=5433 -r odoo -w odoo --db_host=127.0.0.1 --logfile=/src/access.log --logrotate --workers=2 --proxy-mode --no-database-list
fi

# -*- coding: utf-8 -*-
# Copyright 2016 Openworx, LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    "name": "Site Universidade Digital",
    "summary": "Site público Universidade Digital",
    "version": "10.0.1.0.18",
    "category": "Site UD",
    "website": "http://ud.arapiraca.ufal.br",
    "description": """""",
    "author": "NTI UFAL Arapiraca",
    "license": "LGPL-3",
    "installable": True,
    "depends": ['web', 'ud'],
    "data": [
        # Views Frontend
        'views/website.xml',
        'views/colaboradores.xml',
        # Views Backend
        'views/backend/colaborador_view.xml',
        'views/backend/sobre_view.xml',
        'views/backend/menus.xml',

        # Security
        'security/ir.model.access.csv',
    ],
}

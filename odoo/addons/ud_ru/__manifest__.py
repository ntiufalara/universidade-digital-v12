# -*- coding: utf-8 -*-

{
    'name': "Restaurante Universitário",
    'summary': """Restaurante Universitário UD""",
    'description': """
       Módulo responsável pelo controle de refeições do RU
    """,

    'author': "NTI UFAL Arapiraca - Marcos José",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Universidade Digital',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends':  ["ud", "ud_website"],

    # always loaded
    'data': [
        #Demo
        'demo/demo.xml',
        # Segurança
        'security/ud_ru_security.xml',
        'security/ir.model.access.csv',
        # Views
        'views/cadastro.xml',
        'views/templates.xml',
        'views/gru_view.xml',
        'views/movimentacao_view.xml',
        'views/movimentacao_graph_view.xml',
        'views/pessoa_view.xml',
        'views/refeicao_view.xml',
        'views/refeicao_tipo_view.xml',
        'views/restaurante_view.xml',
        'views/responsavel_view.xml',
        'views/menus.xml',

    ],
    "installable": True,
    "application": True,
}


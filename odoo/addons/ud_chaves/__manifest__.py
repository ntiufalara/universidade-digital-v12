# encoding: UTF-8

{
    "name": "Chaves UD",
    "version": "2.0",
    "category": "Universidade Digital",
    "description": """Gerenciador de chaves.""",
    "author": "NTI UFAL Arapiraca",
    "depends": ["ud"],
    "data": [
        # Segurança
        "security/ud_chaves_security.xml",
        "security/ir.model.access.csv",
        # Views
        "views/autorizacao_chave_view.xml",
        "views/chave_view.xml",
        "views/gerente_view.xml",
        "views/registro_chave_view.xml",
        "views/responsavel_view.xml",
        "views/seguranca_view.xml",
        "views/solicitacao_chave_view.xml",
        "views/solicitacao_chave_graph_view.xml",
        "views/transferencia_view.xml",
        # Wizards
        "wizards/adicionar_chave_wiz_view.xml",
        "wizards/remover_chave_wiz_view.xml",
        "wizards/transferir_chave_wiz_view.xml",
        #Menu
        "views/menus.xml",
    ],
    "installable": True,
    "application": True,
}

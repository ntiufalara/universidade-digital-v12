from odoo import models, fields, api


class TipoArCondicionado(models.Model):
    """
    Representa o tipo de ar condicionado a ser selecionado na solicitação de serviço
    """
    _name = 'ud.servico.tipo_ar'
    _order = 'name asc'

    name = fields.Char('Tipo', required=True)

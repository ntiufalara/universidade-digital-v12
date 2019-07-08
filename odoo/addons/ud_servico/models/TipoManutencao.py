from odoo import models, fields


class TipoManutencao(models.Model):
    """
    Representa o tipo de manutenção a ser selecionado na solicitação de serviço
    """
    _name = 'ud.servico.tipo_manutencao'
    _order = 'name asc'

    name = fields.Char('Tipo', required=True)

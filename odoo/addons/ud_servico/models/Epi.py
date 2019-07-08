# encoding: UTF-8

from odoo import models, fields


class Epi(models.Model):
    """
    Representa o cadastro de Equipamentos de Proteção Individual na solicitação de serviço
    """
    _name = 'ud.servico.epi'

    name = fields.Char('Nome', required=True)

    _sql_constraints = [
        ('epi_name_unique', 'unique(name)', "Já existe um EPI com esse mesmo nome.")
    ]

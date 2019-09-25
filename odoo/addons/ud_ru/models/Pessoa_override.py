# encoding: UTF-8
from odoo import models, fields, api


class Pessoa(models.Model):
    """
    Classe que representa os campos do formulário Pessoa.
    """
    _name = 'res.users'
    _inherit = 'res.users'
    _order = 'name asc'

    # restaurante_responsavel_ids = fields.One2many('ud.ru.responsavel', 'pessoa_id',
    #                                                u'Responsável pelo RU')

    saldo = fields.Float(u'Saldo', required=True, default=0.0)

    def incrementar_saldo(self, valor):
        self.saldo += valor;

    def decrementar_saldo(self, valor):
        self.saldo -= valor;


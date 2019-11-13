from odoo import models, fields, api
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)


class Movimentacao(models.Model):
    """
    Movimentação
    """
    _name = 'ud.ru.movimentacao'

    _order = 'id desc'

    codigo = fields.Char('Código', required=True)
    #name = fields.Char('Código', required=True)
    valor = fields.Float('Valor', required=True)

    data_hora = fields.Datetime('Data e hora', default=fields.datetime.now())

    _tipo = [("gru", "GRU"),
              ("trans_rec", "TRANS REC"),
              ("trans_env", "TRANS ENV"),
              ("almoco", "ALMOCO"),
              ("janta", "JANTA"),
              ("estorno", "ESTORNO")]
    tipo = fields.Selection(_tipo, "Tipo")

    pessoa_id = fields.Many2one('res.users', 'Usuário', required=True)#, default=lambda self: self.env.uid
    # funcionario_id = fields.Many2one('res.users', 'Funcionário', default=lambda self: self.env.uid) #quem cria já é pego automaticamente pelo banco

    # _sql_constraints = [
    #     ('name_unico', 'unique (name)', u'GRU já cadastrada!'),
    # ]

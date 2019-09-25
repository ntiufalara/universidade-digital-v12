from odoo import models, fields, api
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)


class Transferencia(models.Model):
    """
    Transferencia
    """
    _name = 'ud.ru.transferencia'

    _order = 'id desc'

    # codigo = fields.Char('Código', required=True)
    valor = fields.Float('Valor', required=True)
    data_transferencia = fields.Date('Data de transferencia', default=fields.date.today(), required=True)#TODO PEGAR A HORA?

    pessoa_id = fields.Many2one('res.users', 'Usuário', required=True, default=lambda self: self.env.uid)
    destinatario_id = fields.Many2one('res.users', 'Destinatário', required=True)

    # _sql_constraints = [
    #     ('name_unico', 'unique (name)', u'Transferencia já cadastrada!'),
    # ]

   

  

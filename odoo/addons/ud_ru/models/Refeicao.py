import logging
from odoo import models, fields, api
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class Refeicao(models.Model):
    """
    Refeicao
    """
    _name = 'ud.ru.refeicao'

    _order = 'id desc'

    name = fields.Char('Código',  readonly=True)#compute='get_name',
    valor = fields.Integer('Valor')
    tipo_refeicao_id = fields.Many2one('ud.ru.tipo_refeicao', 'Tipo da refeição', required=True)#TODO VER O TIPO DE DADOS DE tipo_refeicao_id
    data_hora = fields.Datetime('Data e hora', default=fields.datetime.now())

    pessoa_id = fields.Many2one('res.users', 'Usuário do restaurante')

    # @api.one
    # def get_name(self):
    #     self.name = "R_{}".format(self.id)
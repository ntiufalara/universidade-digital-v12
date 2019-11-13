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

    pessoa_id = fields.Many2one('res.users', 'Usuário', required=True)#, default=lambda self: self.env.uid
    destinatario_id = fields.Many2one('res.users', 'Destinatário', required=True)

    # _sql_constraints = [
    #     ('name_unico', 'unique (name)', u'Transferencia já cadastrada!'),
    # ]

    @api.model
    def create(self, vals):
        """
        Override: Cria a transferencia e as respectivas movimentações.
        :param vals:
        :return:
        """
        #para setar o desinatário a partir do cpf
        if vals.get("cpf"):
            destinatario = self.env['res.users'].sudo().search([('cpf', '=', vals.get("cpf_destinatario"))])
            vals['pessoa_id'] = destinatario.id

        res = super(Transferencia, self).create(vals)

        Movimentacao = self.env['ud.ru.movimentacao']
        movimentacao1_id = Movimentacao.create({
            'codigo': "T_{}".format(res.id),
            'valor': res.valor,
            'tipo': "trans_env",
            'pessoa_id': res.pessoa_id.id,
        })
        movimentacao2_id = Movimentacao.create({
            'codigo': "T_{}".format(res.id),
            'valor': res.valor,
            'tipo': "trans_rec",
            'pessoa_id': res.destinatario_id.id,
        })

        return res

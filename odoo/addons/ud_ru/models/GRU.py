from odoo import models, fields, api
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)


class GRU(models.Model):
    """
    GRU
    """
    _name = 'ud.ru.gru'

    _order = 'id desc'

    # codigo = fields.Char('Código', required=True)
    name = fields.Char('Código', required=True)
    valor = fields.Float('Valor', required=True)
    # obs se falta algo
    data_pagamento = fields.Date('Data de pagamento', default=fields.date.today(), required=True)

    _STATE = [("aguardando", "Aguardando Verificação"),
              ("aprovada", "Aprovada"),
              ("rejeitada", "Rejeitada")]
    state = fields.Selection(_STATE, "Status", default='aguardando')

    pessoa_id = fields.Many2one('res.users', 'Dono da GRU', required=True, default=lambda self: self.env.uid)

    # _sql_constraints = [
    #     ('name_unico', 'unique (name)', u'GRU já cadastrada!'),
    # ]

    # @api.one
    # def cadastrar_gru(self, vals):
    #     obj = super(GRU, self).create(vals)

    @api.model
    def create(self, vals):
        """
        Cria o item GRU caso ele não exista antes de salvar
        :param vals:
        :return:
        """
        obj = super(GRU, self).create(vals)
        # obj.pessoa_id.incrementar_saldo(obj.valor)
        return obj

    @api.one
    def botao_aprovar(self):
        """
        Aprova a GRU
        :return:
        """
        self.pessoa_id.incrementar_saldo(self.valor)
        movimentacao_id = self.env['ud.ru.movimentacao'].create({
            'codigo': "G_{}".format(self.id),
            'valor': self.valor,
            'tipo': "gru",
            'pessoa_id': self.pessoa_id.id,
        })
        self.state = 'aprovada'

    def botao_rejeitar(self):
        """
        Rejeita a GRU
        :return:
        """
        self.state = 'rejeitada'

    # @api.model
    # def create(self, vals):
    #     """
    #     Cria o item no estoque caso ele não exista antes de salvar
    #     :param vals:
    #     :return:
    #     """
    #     obj = super(EstoqueEntrada, self).create(vals)
    #     estoque_model = self.env['ud.almoxarifado.estoque']
    #     # Verifica a condição abaixo (se já existe) para executar a criação de um novo item de estoque
    #     domain_exists = [('almoxarifado_id', '=', obj.almoxarifado_id.id), ('produto_id', '=', obj.produto_id.id)]
    #     estoque_id = estoque_model.search(domain_exists)
    #     if not estoque_id:
    #         # Cria o item de estoque
    #         estoque_id = self.env['ud.almoxarifado.estoque'].create({
    #             'produto_id': obj.produto_id.id,
    #             'estoque_min': 1,
    #             'almoxarifado_id': obj.almoxarifado_id.id,
    #             'campus_id': obj.almoxarifado_id.campus_id.id,
    #             'polo_id': obj.almoxarifado_id.polo_id.id
    #         })
    #     # Atribui o item de estoque à entrada
    #     obj.estoque_id = estoque_id
    #     return obj
    #
    # @api.one
    # def get_name(self):
    #     self.name = "ALM_ENTRADA_{}".format(self.id)
    #

    # @api.constrains('remessa_id', 'almoxarifado_id', 'name')
    # def verifica_almoxarifado(self):
    #     if self.remessa_id and self.almoxarifado_id.id != self.remessa_id.almoxarifado_id.id:
    #         raise ValidationError('O almoxarifado da entrada {} precisa ser o mesmo da remessa'.format(self.name))

# encoding: UTF-8
from odoo import models, fields, api


class Seguranca(models.Model):
    _name = 'ud.chaves.seguranca'

    name = fields.Char(u'Nome', compute='get_name')
    pessoa_id = fields.Many2one('res.users', u'Pessoa', required=True)
    campus_id = fields.Many2one('ud.campus', u'Campus', required=True)
    polo_id = fields.Many2one('ud.polo', u'Polo', required=False)
    is_ativo = fields.Boolean(string=u'Chaves', default=True)

    _sql_constraints = [
        ('pessoa_id_uniq', 'UNIQUE(pessoa_id)',
         "Encontramos outro cadastro para a mesma pessoa, por favor edite ou apague o outro registro pra salvar.")
    ]

    @api.one
    @api.depends('pessoa_id')
    def get_name(self):
        self.name = u"{}".format(self.pessoa_id.name)

    @api.model
    def create(self, vals):
        res = super(Seguranca, self).create(vals)
        group_chave_seguranca = self.env.ref('ud_chaves.group_ud_chaves_seguranca')
        res.pessoa_id.groups_id |= group_chave_seguranca
        return res

    @api.model
    def unlik(self, vals):
        #como pode possuir registros relacionados não deve ser excluido
        group_chave_seguranca = self.env.ref('ud_chaves.group_ud_chaves_seguranca')
        res.pessoa_id.groups_id -= group_chave_seguranca
        return res

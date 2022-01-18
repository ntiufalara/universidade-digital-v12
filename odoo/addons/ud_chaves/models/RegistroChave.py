# encoding: UTF-8
from odoo import models, fields, api


class RegistroChave(models.Model):
    _name = 'ud.chaves.registro_chave'

    _TIPO = [("add", "Adição"),
             ("rem", "Remoção")]

    name = fields.Char(u'Nome', compute='get_name')
    atribuidor_id = fields.Many2one('res.users', u'Gerente')
    responsavel_id = fields.Many2one('ud.chaves.responsavel', 'Responsavel',)
    chave_ids = fields.Many2many('ud.chaves.chave', 'ud_chave_registro_chave_resp_rel', 'registro_chave_id', 'chave_id', string=u'Chaves', required=True)
    tipo = fields.Selection(_TIPO, "Tipo", default='add')

    @api.one
    def get_name(self):
        self.name = u"{} - {}".format(self.id, self.responsavel_id.name)
   

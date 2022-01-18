# encoding: UTF-8

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Chave(models.Model):
    """
    Cadastro de Chave, localização e responsável
    """
    _name = 'ud.chaves.chave'

    _STATE = [("aguardando", "Aguardando"),
              ("entregue", "Entregue"),
              ("disponivel", "Disponível")]

    name = fields.Char(u'Nome', required=True)
    numero = fields.Char(u'Número', required=True)
    campus_id = fields.Many2one('ud.campus', u'Campus', required=True)
    polo_id = fields.Many2one('ud.polo', u'U. Educacional', domain="[('campus_id', '=', campus_id)]", required=True)
    bloco_id = fields.Many2one('ud.bloco', u'Bloco/Prédio', domain="[('polo_id', '=', polo_id)]", required=True)
    observacoes = fields.Text(u'Observações')
    state = fields.Selection(_STATE, "Status", default='disponivel')

    def aguardar(self):
        self.state = 'aguardando'

    def disponibilizar(self):
        self.state = 'disponivel'

    def entregar(self):
        self.state = 'entregue'

    @api.model
    def create(self, vals):
        """
        :param vals:
        :return:
        """
        user = self.env.user
        grupo_admin = self.env.ref('ud_chaves.group_ud_chaves_administrador')
        if grupo_admin not in user.groups_id:
            raise ValidationError('Você não tem permissão para executar essa ação. Por favor entre '
                                  'em contato com administrador do sistema.')

        obj = super(Chave, self).create(vals)
        return obj

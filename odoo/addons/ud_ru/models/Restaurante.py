# encoding: UTF-8

from odoo import models, fields, api


class Restaurante(models.Model):
    """
    Cadastro de restaurante, localização e responsável
    """
    _name = 'ud.ru.restaurante'

    name = fields.Char(u'Nome')
    campus_id = fields.Many2one('ud.campus', u'Campus', required=True)
    polo_id = fields.Many2one('ud.polo', u'Polo', domain="[('campus_id', '=', campus_id)]", required=True)
    observacoes = fields.Text(u'Observações')
    responsavel_ids = fields.Many2many('ud.ru.responsavel', 'ud_ru_responsavel_rel',
                                       string=u'Responsáveis')

    @api.model
    def create(self, vals):
        """
        Caso o usuário não escreva um nome, cira um nome tipo: Restaruante (polo)
        :param vals:
        :return:
        """
        obj = super(Restaurante, self).create(vals)
        if not obj.name:
            obj.name = 'Restaurante {}'.format(obj.polo_id.name)
        return obj

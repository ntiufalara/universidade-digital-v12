from odoo import models, fields


class Colaborador(models.Model):
    _name = 'ud_website.colaborador'
    _description = 'Cadstro de colaboradores do projeto'

    name = fields.Char('Nome completo', required=True)
    descricao = fields.Html('Descrição', sanitize=False)

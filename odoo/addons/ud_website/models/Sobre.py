from odoo import models, fields


class Colaborador(models.Model):
    _name = 'ud_website.sobre'
    _description = 'Texto sobre'

    texto = fields.Html('Texto', sanitize=False)

import logging
from odoo import models, fields, api
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class Refeicao_tipo(models.Model):
    """
    Refeicao_tipo
    """
    _name = 'ud.ru.refeicao_tipo'

    _order = 'id desc'

    name = fields.Char('Nome')
    # codigo = fields.Char('Código')
    valor_aluno_isencao = fields.Float('Aluno com isenção(R$)')
    valor_aluno = fields.Float('Aluno(R$)')
    valor_aluno_pos = fields.Float('Aluno Pós-Graduação(R$)')
    valor_servidor = fields.Float('Servidor(R$)')
    valor_visitante = fields.Float('Visitante(R$)')
    ativo = fields.Boolean(default=True)

    # _sql_constraints = [
    #     ('refeicao_tipo_unica', 'unique (name, valor_aluno, valor_tecnico, valor_docente, valor_visitante)', u'Tipo de refeição já cadastrada!'),
    # ]

    # def get_valor(self, perfil_usuario):
    #     # if
    #     return self.valor_aluno;
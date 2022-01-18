from odoo import models, fields, api
import logging
logger = logging.getLogger(__name__)


class Gerente(models.Model):
    """
    Ao criar este registro, adiciona o gerente ao grupo de permissões atribui um local ao gerente
    """
    _name = 'ud.chaves.gerente'

    _TIPO = [("chave", "Gerente de chave"),
             ("seguranca", "Gerente de segurança")]

    name = fields.Char('Nome', compute='get_name')
    pessoa_id = fields.Many2one('res.users', 'Pessoa', required=True)#, default=lambda self: self.get_pessoa()
    campus_id = fields.Many2one('ud.campus', 'Campus', required=True)
    polo_id = fields.Many2one('ud.polo', 'Polo')
    tipo = fields.Selection(_TIPO, "Tipo", default='chave')
    chave_ids = fields.Many2many('ud.chaves.chave', 'ud_chave_gerente_rel_chave_id', 'gerente_id', 'chave_id',
                                        string=u'Chaves', required=True)
    is_ativo = fields.Boolean(string=u'Chaves', default=True)
    email = fields.Char('E-mail', related='pessoa_id.email')
    celular = fields.Char('Celular', related='pessoa_id.celular')

    _sql_constraints = [
        ('gerente_pessoa_id_uniq', 'UNIQUE(pessoa_id)',
         "Encontramos outro cadastro para a mesma pessoa, por favor edite ou apague o outro registro pra salvar.")
    ]

    @api.one
    def get_name(self):
        self.name = self.pessoa_id.name

    @api.multi
    @api.onchange('tipo')
    def onchange_tipo(self):
        """
        :return:
        """
        group_gerente_de_chave = self.env.ref('ud_chaves.group_ud_chaves_gerente_de_chave')
        group_gerente_de_seguranca = self.env.ref('ud_chaves.group_ud_chaves_gerente_de_seguranca')
                
        if self.tipo == 'chave':
            self.pessoa_id.groups_id |= group_gerente_de_chave
            self.pessoa_id.groups_id -= group_gerente_de_seguranca
        elif self.tipo == 'seguranca':    
            self.pessoa_id.groups_id |= group_gerente_de_seguranca
            self.pessoa_id.groups_id -= group_gerente_de_chave
        
        
    def get_pessoa(self):
        if self.env.context.get('active_model') == 'res.users':
            return self.env.context.get('active_id')
        return False

    @api.model
    def create(self, vals):
        res = super(Gerente, self).create(vals)
        if self.tipo == 'chave':
            group_gerente = self.env.ref('ud_chaves.group_ud_chaves_gerente_de_chave')
        else:    
            group_gerente = self.env.ref('ud_chaves.group_ud_chaves_gerente_de_seguranca')

        res.pessoa_id.groups_id |= group_gerente
        responsavel = self.env['ud.chaves.responsavel'].create(vals)
        return res
    
  
# encoding: UTF-8
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging
logger = logging.getLogger(__name__)

class Responsavel(models.Model):
    _name = 'ud.chaves.responsavel'

    name = fields.Char(u'Nome', compute='get_name')
    pessoa_id = fields.Many2one('res.users', u'Pessoa', required=True)
    campus_id = fields.Many2one('ud.campus', u'Campus', required=True)
    polo_id = fields.Many2one('ud.polo', u'Polo', required=False)
    chave_ids = fields.Many2many('ud.chaves.chave', 'ud_chave_responsavel_rel_chave_id', 'responsavel_id', 'chave_id',
                    string=u'Chaves', domain=lambda self:self.domain_chaves_gerente())#, required=True   domain=lambda self:self.domain_chaves_gerente()
    is_ativo = fields.Boolean(string=u'Chaves', default=True)
   
    email = fields.Char('E-mail', related='pessoa_id.email')
    celular = fields.Char('Celular', related='pessoa_id.celular')

    _sql_constraints = [
        ('responsavel_pessoa_id_uniq', 'UNIQUE(pessoa_id)',
         "Encontramos outro cadastro para a mesma pessoa, por favor edite ou apague o outro registro pra salvar.")
    ]

    @api.one
    @api.depends('pessoa_id')
    def get_name(self):
        self.name = u"{}".format(self.pessoa_id.name)
   
    def domain_chaves_gerente(self):
        """
        Localiza o objeto "gerente" para o usuário e retorna as chaves associadas. 
        Utilizado na filtragem de chaves pelo gerente.
        :return:
        """
        user = self.env.user
        grupo_gerente_chave = self.env.ref('ud_chaves.group_ud_chaves_gerente_de_chave')
        grupo_admin = self.env.ref('ud_chaves.group_ud_chaves_administrador')
        domain = []   
        
        if grupo_gerente_chave in user.groups_id and grupo_admin not in user.groups_id:
            gerente = self.env['ud.chaves.gerente'].search([
                ('pessoa_id', '=', self.env.uid)
            ])
            
            chave_ids = [chave.id for chave in gerente.chave_ids]
            domain = [('id', 'in', list(chave_ids))]

        elif grupo_admin not in user.groups_id:
            domain = [('id', 'in', [])]
        return domain

    def process_domain(self):
        """
        Usado para filtrar apenas com itens aos quais o responsável tem acesso.
        :return: [(), (),...]
        """

        user = self.env.user
        grupo_admin = self.env.ref('ud_chaves.group_ud_chaves_administrador')
        grupo_gerente_chave = self.env.ref('ud_chaves.group_ud_chaves_gerente_de_chave')
        grupo_seguranca = self.env.ref('ud_chaves.group_ud_chaves_seguranca')
        grupo_gerente_seguranca = self.env.ref('ud_chaves.group_ud_chaves_gerente_de_seguranca')
        
        domain = []
        if grupo_admin not in user.groups_id and grupo_gerente_chave in user.groups_id:
            gerente = self.env['ud.chaves.gerente'].search([
                    ('pessoa_id', '=', user.id)
                ])
            if not gerente:
                raise ValidationError('Você não possui permissão para solicitar essa ação, '
                                    'em caso de dúvidas contate o administrador do sistema')

            chaves_gerente = []
            for chave in gerente.chave_ids:
                chaves_gerente.append(chave.id)
            domain.append(('chave_ids', 'in', list(chaves_gerente)))         

        elif grupo_admin not in user.groups_id and grupo_seguranca in user.groups_id:
            seguranca = self.env['ud.chaves.seguranca'].search([
                    ('pessoa_id', '=', user.id)
                ])
            domain.append(('polo_id', '=', seguranca.polo_id.id))

        elif grupo_admin not in user.groups_id and grupo_gerente_seguranca in user.groups_id:
            gerente = self.env['ud.chaves.gerente'].search([
                    ('pessoa_id', '=', user.id)
                ])
            domain.append(('polo_id', '=', gerente.polo_id.id))
                
        return domain
      
    @api.model
    def create(self, vals):
        res = super(Responsavel, self).search([('pessoa_id', '=', vals.get('pessoa_id'))])
        chave_vals = list(vals.get('chave_ids'))[0][2]

        if (len(chave_vals) == 0):
            raise ValidationError('Selecione uma chave.') 

        if not res.exists():
            res = super(Responsavel, self).create(vals)     
        
        #lista com as chaves que o responsável deve ter acesso
        chaves_list = [chave.id for chave in res.chave_ids]
            
        for id in chave_vals:
            chaves_list.append(id)

        res.sudo().write({
            'chave_ids': [(6, 0, chaves_list)],
        })
        
        registro_chave = self.env['ud.chaves.registro_chave'].create({
                'atribuidor_id': self.env.uid,
                'chave_ids': [(6, False, chave_vals)],
                'responsavel_id': res.id,
                'tipo': 'add'
            })     

     
        group_usuario_chave = self.env.ref('ud_chaves.group_ud_chaves_responsavel')
        res.pessoa_id.groups_id |= group_usuario_chave
        return res

  
    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        domain = [] if not domain else domain
        domain += self.process_domain()
        return super(Responsavel, self).search_read(domain, fields, offset, limit, order)
   
    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        """
        Sobrescrito para considerar o domain baseado no ``filtra_responsavel``
        Adiciona ('dia_ids.espaco_id', 'in', <lista de espaços sob responsabilidade do usuário>)
        :param domain:
        :param fields:
        :param groupby:
        :param offset:
        :param limit:
        :param orderby:
        :param lazy:
        :return:
        """
        domain = [] if not domain else domain
        domain += self.process_domain()     
        return super(Responsavel, self).read_group(domain, fields, groupby, offset, limit, orderby, lazy)

  
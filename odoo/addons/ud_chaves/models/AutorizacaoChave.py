from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging
logger = logging.getLogger(__name__)


class AutorizacaoChave(models.Model):
    """
    Registro de autorizacao de emprestimo de chave.
    """
    _name = 'ud.chaves.autorizacao'
    _order = 'id desc'

    # ("nova", "Nova"),
    _STATE = [("aguardando", "Aguardando Retirada"),
              ("entregue", "Entregue"),
              ("devolvida", "Devolvida"),
              ("cancelada", "Cancelada")]

    name = fields.Char('Código', compute='get_name', readonly=True)
    solicitante_id = fields.Many2one('ud.chaves.responsavel', 'Solicitante', ondelete='restrict', 
                    default=lambda self: self.get_solicitante())#,default=lambda self: self.env.uid 
    seguranca_entregou_id = fields.Many2one('ud.chaves.seguranca', 'Quem entregou', ondelete='restrict')#,default=lambda self: self.env.uid 
    seguranca_recebeu_id = fields.Many2one('ud.chaves.seguranca', 'Quem recebeu', ondelete='restrict')#,default=lambda self: self.env.uid 
    chave_ids = fields.Many2many('ud.chaves.chave', 'chave_autorizacao_rel', string=u'Chaves', 
                                  required=True, domain=lambda self: self.domain_chaves_responsavel())
    data_hora = fields.Datetime('Data/hora da solicitação', default=fields.datetime.now(), readonly=True)
    data_hora_entrega = fields.Datetime('Data/hora da entrega', readonly=True)
    data_hora_devolucao = fields.Datetime('Data/hora da devolução', readonly=True)
    state = fields.Selection(_STATE, "Status", default='aguardando', readonly=True)
    polo_id = fields.Many2one('ud.polo', 'U. Educacional', compute='get_polo', store=True)
    email = fields.Char('E-mail', related='solicitante_id.email')
    celular = fields.Char('Celular', related='solicitante_id.celular')
    
    detalhes = fields.Text('Detalhes')
    observacoes_segurança = fields.Text('Observações do segurança')

    def get_solicitante(self):
        responsavel = self.env['ud.chaves.responsavel'].search([
            ('pessoa_id', '=', self.env.uid)
        ])
        return responsavel

    def get_seguranca(self):
        seguranca = self.env['ud.chaves.seguranca'].search([
            ('pessoa_id', '=', self.env.uid)
        ])
        # TODO SE SEGURANÇA NULO, LANCAR ERRO?
        return seguranca

    @api.one
    @api.depends('solicitante_id')
    def get_polo(self):
        """
        Carrega o Polo atrelado ao solicitante
        :return:
        """
        self.polo_id = self.solicitante_id.polo_id.id
        
       

    def domain_chaves_responsavel(self):
        """
        Localiza o objeto "responsavel" para o usuário e retorna o domain das chaves associadas
        :return:
        """
        responsavel = self.env['ud.chaves.responsavel'].search([
            ('pessoa_id', '=', self.env.uid)
        ])
        chave_ids = [chave.id for chave in responsavel.chave_ids]
        domain = [('id', 'in', list(chave_ids))]
        return domain

  

    def chaves_responsavel(self):
        """
        Localiza o objeto "responsavel" para o usuário e retorna uma lista das chaves associadas
        :return:
        """
        responsavel = self.env['ud.chaves.responsavel'].search([
            ('pessoa_id', '=', self.env.uid)
        ])

        chave_ids = [chave.id for chave in responsavel.chave_ids]
        return chave_ids

    def chaves_gerente(self):
        """
        Localiza o objeto "gerente" para o usuário e retorna as chaves associadas
        :return:
        """
        gerente = self.env['ud.chaves.gerente'].search([
            ('pessoa_id', '=', self.env.uid)
        ])

        chave_ids = [chave.id for chave in gerente.chave_ids]
        return chave_ids
    

    def process_domain(self):
        """
        Usado para filtrar apenas com itens aos quais o responsável tem acesso.
        :return: [(), (),...]
        """
        domain = []
    
        if self.env.context.get('filtrar_solicitante_responsavel'):
            responsavel = self.env['ud.chaves.responsavel'].search([
                ('pessoa_id', '=', self.env.uid)
            ])
            domain.append(('solicitante_id', '=', responsavel.id))
            
        if self.env.context.get('filtrar_por_chaves'):
            chaves = set(self.chaves_responsavel()) | set(self.chaves_gerente())
            domain.append(('chave_ids', 'in', list(chaves)))
            
        if self.env.context.get('filtrar_por_polo'):
            seguranca = self.env['ud.chaves.seguranca'].search([
                ('pessoa_id', '=', self.env.uid)
            ])
            domain.append(('polo_id', '=', seguranca.polo_id.id))
         
        return domain

    

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        domain = [] if not domain else domain
        # domain += self.filtrar_solicitante_responsavel()
        domain += self.process_domain()
        return super(AutorizacaoChave, self).search_read(self.process_domain(), fields, offset, limit, order)
   
    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        """
        Sobrescrito para considerar o domain baseado no 'filtrar_solicitante_responsavel', 'filtrar_por_chaves' e 'filtrar_por_polo'.
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
        # domain += self.filtrar_solicitante_responsavel()
        domain += self.process_domain()
        return super(AutorizacaoChave, self).read_group(domain, fields, groupby, offset, limit, orderby, lazy)

    @api.one
    def get_name(self):
        self.name = "CH_SLC_{}".format(self.id)

    def botao_entregar(self):
        """
        Altera o status da solicitação para 'entregue'
        :return:
        """
        for chave in self.chave_ids:
            chave.entregar()  
        self.state = 'entregue'
        self.data_hora_entrega = fields.datetime.now()
        self.seguranca_entregou_id = self.get_seguranca()

    def botao_devolver(self):
        """
        Conclui a solicitação com o status 'devolvida'
        :return:
        """
        for chave in self.chave_ids:
            chave.disponibilizar()  
        self.state = 'devolvida'
        self.data_hora_devolucao = fields.datetime.now()
        self.seguranca_recebeu_id = self.get_seguranca()

    def botao_cancelar(self):
        """
        Cancela a solicitação.
        :return:
        """
        self.state = 'cancelada'



# encoding: UTF-8

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging
logger = logging.getLogger(__name__)

class Transferencia(models.Model):
    """
    Cadastro de Transferencia
    """
    _name = 'ud.chaves.transferencia'

    _STATE = [("cancelada", "Cancelada"),
              ("finalizada", "Finalizada"), 
              ("aguardando", "Aguardando")]

    name = fields.Char('Código', compute='get_name', readonly=True)
    solicitacao_id = fields.Many2one('ud.chaves.solicitacao', 'Solicitação', ondelete='restrict',)
    solicitante_id = fields.Many2one('ud.chaves.responsavel', 'Recebedor', ondelete='restrict',)
    transferidor_id = fields.Many2one('ud.chaves.responsavel', 'Transferente', ondelete='restrict', 
                    default=lambda self: self.get_solicitante())#,default=lambda self: self.env.uid 
    state = fields.Selection(_STATE, "Estado", default='aguardando')


    # by default store = False this means the value of this field
    # is always computed.
    current_user = fields.Many2one('ud.chaves.responsavel', compute='_get_current_user')
    is_transferidor = fields.Boolean('É transferidor', compute='_get_is_transferidor')

    


    @api.depends('solicitante_id')
    def _get_current_user(self):
        responsavel = self.env['ud.chaves.responsavel'].search([
            ('pessoa_id', '=', self.env.uid)
        ])
        for rec in self:
            rec.current_user = responsavel
        # self.current_user = 1

    @api.depends('solicitante_id')
    def _get_is_transferidor(self):
        responsavel_user = self.env['ud.chaves.responsavel'].search([
            ('pessoa_id', '=', self.env.uid)
        ])

        if self.solicitante_id == responsavel_user:
            self.is_transferidor = True
        else:
            self.is_transferidor = False


    @api.one
    def get_name(self):
        self.name = "TR_{}".format(self.id)

    def get_current_uid(self):
        """  
        :param self: 
        :return: 
        """
        responsavel = self.env['ud.chaves.responsavel'].search([
            ('pessoa_id', '=', self.env.uid)
        ])
               
        self.manager_id = responsavel
    
    @api.model
    @api.one
    def is_solicitante(self):
        responsavel = self.env['ud.chaves.responsavel'].search([
            ('pessoa_id', '=', self.env.uid)
        ])
        return responsavel == self.solicitante_id

    def get_solicitante(self):
        responsavel = self.env['ud.chaves.responsavel'].search([
            ('pessoa_id', '=', self.env.uid)
        ])
        return responsavel

    def cancelar(self):
        self.state = 'cancelada'

    def aceitar(self):

        responsavel = self.env['ud.chaves.responsavel'].search([
            ('pessoa_id', '=', self.env.uid)
        ])
        if responsavel != self.solicitante_id:
            raise ValidationError('Apenas o solicitante que pode aceitar a transferência.')
       
        self.state = 'finalizada'
        chaves_add = [chave.id for chave in self.solicitacao_id.chave_ids]    

        solicitacao_nova = self.env['ud.chaves.solicitacao'].create({#sudo().
                    'state': 'entregue', 
                    'chave_ids': [(6, False, chaves_add)],
                    'quem_entregou_id': self.transferidor_id.pessoa_id.id,
                    'solicitante_id': self.solicitante_id.id,
                    })

        self.solicitacao_id.botao_transferir()

       
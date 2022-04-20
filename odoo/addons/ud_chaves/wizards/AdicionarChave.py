# encoding: UTF-8

from odoo import models, fields, api
import logging
logger = logging.getLogger(__name__)

class AdicionarChave(models.TransientModel):
    """
    Usado no Wizard para adicionar chave a um responsável.
    """
    _name = 'ud.chaves.adicionar_chave'

    chave_ids = fields.Many2many('ud.chaves.chave', 'ud_adicionar_chave_responsavel_rel_wiz', 
    'responsavel_id', 'chave_id', string=u'Chaves para Adicionar:', 
        domain=lambda self:self.domain_chaves_gerente(), required=True)

    def domain_chaves_gerente(self):

        user = self.env.user
        grupo_admin = self.env.ref('ud_chaves.group_ud_chaves_administrador')
        responsavel = self.env['ud.chaves.responsavel'].browse(self.env.context.get('active_id'))

        if grupo_admin in user.groups_id: #TODO Testar
            # domain = []
            chave_ids = [chave.id for chave in responsavel.chave_ids]
            domain = [('id', 'not in', list(chave_ids))]
        else:    
            # responsavel = self.env['ud.chaves.responsavel'].browse(self.env.context.get('active_id'))
            gerente = self.env['ud.chaves.gerente'].search([
                    ('pessoa_id', '=', self.env.uid)
                ])
            #para exibir apenas as chaves que o responsável não tem    
            chaves_inter = gerente.chave_ids - responsavel.chave_ids  
            chave_ids = [chave.id for chave in chaves_inter]
            domain = [('id', 'in', list(chave_ids))]
                   
        return domain

    def adicionar(self):
        if len(self.chave_ids) > 0:      
            responsavel_id = self.env.context.get('active_id')
            responsavel = self.env['ud.chaves.responsavel'].browse(responsavel_id)
            
            chaves = responsavel.chave_ids | self.chave_ids
            #lista com as chaves que o responsável deve ter acesso
            chaves_list = [chave.id for chave in chaves]

            #apenas as novas chaves adicionadas
            chaves_add = [chave.id for chave in self.chave_ids]
            registro_chave = self.env['ud.chaves.registro_chave'].create({
                'atribuidor_id': self.env.uid,
                'chave_ids': [(6, False, chaves_add)],
                'responsavel_id': responsavel_id,
                'tipo': 'add',
            })
            responsavel.sudo().write({
                'chave_ids': [(6, 0, chaves_list)],
            })
      

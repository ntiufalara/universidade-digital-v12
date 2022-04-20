# encoding: UTF-8

from odoo import models, fields, api
import logging
logger = logging.getLogger(__name__)

class RemoverChave(models.TransientModel):
    """
    Usado no Wizard para remover chave de um responsável
    """
    _name = 'ud.chaves.remover_chave'

    chave_ids = fields.Many2many('ud.chaves.chave', 'ud_chave_responsavel_rel_wiz', 
    'responsavel_id', 'chave_id', string=u'Chaves para REMOVER:', 
        domain=lambda self:self.domain_chaves_gerente())

    def domain_chaves_gerente(self):
        user = self.env.user
        grupo_admin = self.env.ref('ud_chaves.group_ud_chaves_administrador')
        responsavel = self.env['ud.chaves.responsavel'].browse(self.env.context.get('active_id'))

        if grupo_admin in user.groups_id: 
            # domain = []
            chave_ids = [chave.id for chave in responsavel.chave_ids]
            domain = [('id', 'in', list(chave_ids))]
            
        else: 
            # responsavel = self.env['ud.chaves.responsavel'].browse(self.env.context.get('active_id'))
            gerente = self.env['ud.chaves.gerente'].search([
                    ('pessoa_id', '=', self.env.uid)
                ])
            chaves_inter = responsavel.chave_ids & gerente.chave_ids  
            
            chave_ids = [chave.id for chave in chaves_inter]
            domain = [('id', 'in', list(chave_ids))]
        return domain

    def remover(self):

        if len(self.chave_ids):
            responsavel_id = self.env.context.get('active_id')
            responsavel = self.env['ud.chaves.responsavel'].browse(responsavel_id)
            
            chaves = responsavel.chave_ids - self.chave_ids
            chaves_list = [chave.id for chave in chaves]

            #NOVA
            chaves_rem = [chave.id for chave in self.chave_ids]
            registro_chave = self.env['ud.chaves.registro_chave'].create({
                'atribuidor_id': self.env.uid,
                'chave_ids': [(6, False, chaves_rem)],
                'responsavel_id': responsavel_id,
                'tipo': 'rem',
            })
            responsavel.sudo().write({
                'chave_ids': [(6, 0, chaves_list)],
            })
        

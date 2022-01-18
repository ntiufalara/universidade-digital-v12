# encoding: UTF-8

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging
logger = logging.getLogger(__name__)

class TransferirChave(models.TransientModel):
    """
    Usado no Wizard para transferir chave a um responsável.
    """
    _name = 'ud.chaves.transferir_chave'

    solicitacao_id = fields.Many2one('ud.chaves.solicitacao', 'Solicitação', ondelete='restrict', 
                    default=lambda self: self.set_solicitacao())#,default=lambda self: self.env.uid 
    responsavel_id = fields.Many2one('ud.chaves.responsavel', 'Solicitante', ondelete='restrict', 
                    domain=lambda self: self.domain_responsaveis())#,default=lambda self: self.env.uid 

    def check_solicitacao_da_transferencia(self):
        if self.solicitacao_id.state != 'entregue':
            raise ValidationError("A transferencia não pode ser realizada por causa do estado atual da solicitação.")
        else:
            # '&',('solicitacao_id', '=', self.solicitacao_id.id), ('state', '=', 'aguardando')
            transferencias = self.env['ud.chaves.transferencia'].search([
                ('solicitacao_id', '=', self.solicitacao_id.id)
            ])
            for transferencia in transferencias:
                logger.error('transferencia.id #########')
                logger.error(transferencia.id)
                if (transferencia.state == 'aguardando'):
                    raise ValidationError("Já existe um pedido de transfência aberto para essa solicitação.")
           
        chaves = self.solicitacao_id.chave_ids
        chaves_responsavel = self.responsavel_id.chave_ids
        if chaves not in chaves_responsavel:
            raise ValidationError("Responsável selecionado não possui permissão para pegar pelo menos uma chave.")


    def set_solicitacao(self):
        solicitacao = self.env['ud.chaves.solicitacao'].browse(self.env.context.get('active_id'))
        return solicitacao

    def domain_responsaveis(self):
        #pega do banco pois ocorreram uns erros quando pegava de self.solicitacao_id
        solicitacao_id = self.env['ud.chaves.solicitacao'].browse(self.env.context.get('active_id'))
        domain = []
        for chave in self.solicitacao_id.chave_ids:
            domain.append(('chave_ids', 'in', [chave.id]))
        # chaves = set(self.chaves_responsavel()) | set(self.chaves_gerente())
        # domain.append(('chave_ids', 'in', list(chaves)))

        return domain
 
    def transferir(self):
        self.check_solicitacao_da_transferencia()
        responsavel = self.env['ud.chaves.responsavel'].search([
            ('pessoa_id', '=', self.env.uid)
        ])

        chaves_add = [chave.id for chave in self.solicitacao_id.chave_ids]
        transferir_chave = self.env['ud.chaves.transferencia'].create({
                'transferidor_id': responsavel.id,
                # 'chave_ids': [(6, False, chaves_add)],
                'solicitante_id': self.responsavel_id.id,
                'solicitacao_id': self.solicitacao_id.id,
            })

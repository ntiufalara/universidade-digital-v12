# encoding: UTF-8

from odoo import models, fields


class Transferir(models.TransientModel):
    """
    Execução e criação da transferencia.
    """
    _name = 'ud.ru.transferir'

    # codigo = fields.Char('Código', required=True)
    valor = fields.Float('Valor', required=True)
    data_transferencia = fields.Date('Data de transferencia', default=fields.date.today(), required=True)  # TODO PEGAR A HORA?

    pessoa_id = fields.Many2one('res.users', 'Usuário', required=True, default=lambda self: self.env.uid)
    destinatario_id = fields.Many2one('res.users', 'Destinatário', required=True)

    def transferir(self): #ver como setar o uid a partir do cpf
        Transferencia = self.env['ud.ru.transferencia']
        transferencia_id = Transferencia.create({
            'valor': self.valor,
            'pessoa_id': self.pessoa_id,
            'destinatario_id': self.destinatario_id,
            'data_transferencia': self.data_transferencia,
        })
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ProdutoQuantidade(models.Model):
    """
    Associa produto à quantidade na solicitação
    """
    _name = 'ud.almoxarifado.produto.qtd'

    name = fields.Char('Nome', compute='get_name')
    quantidade = fields.Integer('Quantidade', required=True)
    categoria_id = fields.Many2one('ud.almoxarifado.produto.categoria', 'Categoria', ondelete='restrict',
                                   required=True)
    campus_id = fields.Many2one('ud.campus', 'Campus', required=True)
    polo_id = fields.Many2one('ud.polo', 'Polo', required=True, domain="[('campus_id', '=', campus_id)]")
    almoxarifado_id = fields.Many2one('ud.almoxarifado.almoxarifado', 'Almoxarifado', required=True,
                                      domain="[('polo_id', '=', polo_id)]")
    estoque_id = fields.Many2one('ud.almoxarifado.estoque', 'Produto', required=True,
                                 domain="[('almoxarifado_id', '=', almoxarifado_id), "
                                        "('categoria_id', '=', categoria_id)]")
    qtd_estoque = fields.Integer('Qtd em estoque', related='estoque_id.quantidade', readonly=True)
    solicitacao_id = fields.Many2one('ud.almoxarifado.solicitacao', 'Solicitação', invisible=True)

    _sql_constraints = [
        ('produto_solicitacao_uniq', 'unique(solicitacao_id,estoque_id)',
         'Não pode solicitar o memo produto na mesma solicitação'),
    ]

    @api.one
    def get_name(self):
        self.name = self.estoque_id.name

    @api.constrains('quantidade')
    def valida_quantidade(self):
        """
        Verifica se a quantidade solicitada está disponível no estoque
        :return:
        """
        if self.quantidade > self.estoque_id.quantidade:
            raise ValidationError("A quantidade para: {} não está disponível no estoque".format(self.estoque_id.name))

    @api.model
    def create(self, vals_list):
        """
        Ao criar solicitação, realiza saída do estoque
        :param vals_list:
        :return:
        """
        saida_model = self.env['ud.almoxarifado.saida']
        obj = super(ProdutoQuantidade, self).create(vals_list)
        saida_model.sudo().create({
            'quantidade': obj.quantidade,
            'estoque_id': obj.estoque_id.id,
            'solicitacao_id': obj.solicitacao_id.id,
            'observacao': 'Nova solicitação'
        })
        return obj

    def write(self, vals):
        """
        Ao alterar a quantidade, registra nova entrada ou saída
        :param vals: dict
        :return: result: boolean
        """
        nova_quantidade = vals.get('quantidade')
        antiga_quantidade = self.quantidade
        result = super(ProdutoQuantidade, self).write(vals)
        if nova_quantidade < antiga_quantidade:
            diferenca = antiga_quantidade - nova_quantidade
            # Realiza entrada
            entrada_model = self.env['ud.almoxarifado.entrada']
            e = entrada_model.sudo().create({
                'quantidade': diferenca,
                'estoque_id': self.estoque_id.id,
                'produto_id': self.estoque_id.produto_id.id,
                'almoxarifado_id': self.almoxarifado_id.id,
                'solicitacao_id': self.solicitacao_id.id,
                'observacao': 'Alteração na solicitação',
                'tipo': 'devolucao'
            })
        if nova_quantidade > antiga_quantidade:
            diferenca = nova_quantidade - antiga_quantidade
            # Realiza saída
            saida_model = self.env['ud.almoxarifado.saida']
            saida_model.sudo().create({
                'quantidade': diferenca,
                'estoque_id': self.estoque_id.id,
                'solicitacao_id': self.solicitacao_id.id,
                'observacao': 'Alteração na solicitação'
            })
        return result

    def unlink(self):
        """
        Ao apagar um item da solicitação, realiza reposição do estoque
        :return:
        """
        entrada_model = self.env['ud.almoxarifado.entrada']
        for produto_qtd in self:
            entrada_model.sudo().create({
                'quantidade': produto_qtd.quantidade,
                'estoque_id': produto_qtd.estoque_id.id,
                'produto_id': produto_qtd.estoque_id.produto_id.id,
                'almoxarifado_id': produto_qtd.almoxarifado_id.id,
                'solicitacao_id': produto_qtd.solicitacao_id.id,
                'observacao': 'Solicitação apagada',
                'tipo': 'devolucao'
            })
        return super(ProdutoQuantidade, self).unlink()

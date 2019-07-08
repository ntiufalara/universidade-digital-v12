# encoding: UTF-8

from odoo import models, fields, api
from odoo.addons.ud_servico.models import utils


# https://segurancadotrabalhonwn.com/como-fazer-ordem-de-servico/
class SolicitacaoServico(models.Model):
    """
    Solicitação para geração de ordem de serviço
    """
    _name = 'ud.servico.solicitacao'
    _description = 'Solicitação de serviço'
    _order = 'data desc'

    _inherit = ['mail.thread']
    _track = {
        'state': lambda self: self.state is not False
    }

    name = fields.Char('Código', compute="get_name")
    solicitante_id = fields.Many2one('res.users', 'Solicitante', required=True, default=lambda self: self.env.uid)
    matricula = fields.Char('Matrícula', compute='get_matricula')
    setor_id = fields.Many2one('ud.setor', 'Setor', compute='get_setor')
    email = fields.Char('E-mail', related='solicitante_id.email')
    telefone = fields.Char('Telefone', related='solicitante_id.telefone_fixo')
    data = fields.Datetime('Data/hora', readonly=True, default=fields.datetime.now())
    state = fields.Selection(utils.STATUS, 'Status', default='nova', track_visibility='onchange')
    descricao = fields.Text('Descrição', required=True)
    revisao = fields.Integer('Revisão', default=1)
    nome_gerente = fields.Char('Gerente', compute='get_nome_gerente', store=True)
    # Segurança no trabalho
    risco_de_operacao = fields.Text('Risco de operação')
    medidas_preventivas = fields.Text('Medidas preventivas')
    epi_ids = fields.Many2many('ud.servico.epi', 'servico_solicitacao_epi', string='EPI')
    # Valores de execução de serviço e cancelamento
    data_cancelamento = fields.Datetime('Data de cancelamento')
    motivo_cancelamento = fields.Text('Motivo cancelamento')
    responsavel_analise_id = fields.Many2one('ud.servico.responsavel', 'Responsável por análise', ondelete='restrict')
    responsavel_execucao_id = fields.Many2one('ud.servico.responsavel', 'Responsável por execução',
                                              ondelete='restrict')
    previsao = fields.Date('Previsão para execução')
    execucao = fields.Text('Descrição do serviço')
    data_execucao = fields.Datetime('Data/hora execução')
    finalizar = fields.Text('Serviço executado')
    # Classificação das ordens de serivço
    tipo_manutencao_id = fields.Many2one('ud.servico.tipo_manutencao', 'Manutenção', required=True)
    tipo_equipamento_id = fields.Many2one('ud.servico.tipo_equipamento', 'Equipamentos')
    tipo_equipamento_eletrico_id = fields.Many2one('ud.servico.tipo_equipamento_eletrico', 'Equipamento elétrico')
    tipo_refrigerador_id = fields.Many2one('ud.servico.tipo_refrigerador', 'Refrigerador')
    tipo_ar_condicionado_id = fields.Many2one('ud.servico.tipo_ar', 'Ar condicionado')
    marca_equipamento = fields.Char('Marca')
    modelo_equipamento = fields.Char('Modelo')
    tipo_predial_id = fields.Many2one('ud.servico.tipo_predial', 'Tipo')
    tipo_instalacoes_id = fields.Many2one('ud.servico.tipo_instalacoes', 'Instalações')
    denominacao = fields.Char('Denominação')
    numero_patrimonio = fields.Char('Patrimônimo nº')
    # Local
    campus_id = fields.Many2one('ud.campus', 'Campus', required=True, default=lambda self: self.get_campus())
    polo_id = fields.Many2one('ud.polo', 'Polo', required=True, domain="[('campus_id', '=', campus_id)]",
                              default=lambda self: self.get_polo())
    espaco_id = fields.Many2one('ud.espaco', 'Espaço', required=True, domain="[('polo_id', '=', polo_id)]")
    bloco_id = fields.Many2one('ud.bloco', 'Bloco', related='espaco_id.bloco_id')
    detalhes_espaco = fields.Char('Detalhes do espaço')
    # Destino de movoimentação de materiais
    campus_destino_id = fields.Many2one('ud.campus', 'Campus')
    polo_destino_id = fields.Many2one('ud.polo', 'Polo', domain="[('campus_id', '=', campus_destino_id)]")
    espaco_destino_id = fields.Many2one('ud.espaco', 'Espaço', domain="[('polo_id', '=', polo_destino_id)]")
    bloco_destino_id = fields.Many2one('ud.bloco', 'Bloco', related='espaco_destino_id.bloco_id')
    detalhes_espaco_destino = fields.Char('Detalhes do espaço')

    @api.one
    def get_name(self):
        self.name = 'SRV_SLC_{}'.format(self.id)

    @api.one
    def get_matricula(self):
        """
        Localiza e atribui a ultima matrícula cadastrada
        :return:
        """
        for papel in self.env.user.perfil_ids:
            self.matricula = papel.matricula
            break

    @api.one
    def get_setor(self):
        """
        Localiza e atribui o setor da última matricula cadastrada
        :return:
        """
        for papel in self.env.user.perfil_ids:
            self.setor_id = papel.setor_id
            break

    def get_campus(self):
        """
        Carrega o Campus atrelado a matricula do usuário por padrão
        :return:
        """
        for papel in self.env.user.perfil_ids:
            return papel.setor_id.polo_id.campus_id.id
        return False

    def get_polo(self):
        """
        Carrega o Polo atrelado a matricula do usuário por padrão
        :return:
        """
        for papel in self.env.user.perfil_ids:
            return papel.setor_id.polo_id.id
        return False

    @api.one
    @api.depends('campus_id', 'polo_id')
    def get_nome_gerente(self):
        """
        Carrega o gerente do local onde a solicitação foi criada
        :return:
        """
        gerente_model = self.env['ud.servico.gerente']
        # Busca pelo gerente na sequência: Gerente do polo, Gerente do campus
        gerente = gerente_model.search([
            ('polo_id', '=', self.polo_id.id)
        ])
        gerente = gerente_model.search([('campus_id', '=', self.campus_id.id)]) if not gerente else gerente
        if gerente:
            gerente.ensure_one()
            self.nome_gerente = gerente.name

    @api.model
    def create(self, vals):
        """
        Override: Atribuindo gerente ao acompanhamento da solicitação; Envia e-mail para o Gerente sobre nova
        solicitação criada.
        :param vals:
        :return:
        """
        # Busca o responsável por solicitações de serviço no Campus e Polo e adiciona para seguir a solicitação
        res = super(SolicitacaoServico, self.with_context(mail_create_nolog=True)).create(vals)
        # Prioriza o gerente do Polo, caso não exista, adiciona o gerente do campus aos seguidores
        gerentes = self.env['ud.servico.gerente'].search([('polo_id', '=', res.polo_id.id)])
        gerentes = self.env['ud.servico.gerente'].search(
            [('campus_id', '=', res.campus_id.id)]) if not gerentes else gerentes
        if gerentes:
            # Se existirem gerentes cadastrados, assina na lista de interesse
            gerentes_user_ids = [gerente.pessoa_id.id for gerente in gerentes]
            res.sudo().message_subscribe_users(gerentes_user_ids)
        messagem = """
        <p>Nova solicitação de serviço criada</p>
        <span><strong>Tipo de manutenção: </strong></span><span>{}</span><br>
        <span><strong>Espaço: </strong></span><span>{}</span><br>
        <span><strong>Solicitante: </strong></span><span>{}</span><br>
        <span><strong>Telefone do solicitante: </strong></span><span>{}</span><br>
        <span><strong>E-mail do solicitante: </strong></span><span>{}</span><br>
        <span><strong>Descrição: </strong></span><span>{}</span><br>
        """.format(res.tipo_manutencao_id.name, res.espaco_id.name, res.solicitante_id.name, res.telefone, res.email,
                   res.descricao)
        res.message_post(messagem, message_type='email', subtype='mt_comment')
        return res

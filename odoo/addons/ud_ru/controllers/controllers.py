# -*- coding: utf-8 -*-
from odoo import http

import logging
_logger = logging.getLogger(__name__)

class UdRu(http.Controller):
    @http.route('/ud_ru/ud_ru/', auth='user', website=True)
    def index(self, **kw):
        return http.request.render('ud_ru.index', {  })

    @http.route('/teste/', auth='user', website=True)
    def teste(self, **kw):
        import csv
        arquivo = open('/ud_ru/security/ir.model.access.csv')

        linhas = csv.reader(arquivo)

        _logger.info("---------------")
        for linha in linhas:
            _logger.info(linha)
        _logger.info("---------------")

        return "CSV OK!"

    @http.route('/cadastrar/', auth='user', website=True)
    def cadastrar(self, **kw):

        if kw.get('cpf'):
            _logger.info("CADASTRADO")
             #     kw['login'] = kw.get('cpf')
            return http.request.render('ud_ru.cadastro', {
                # 'grus': grus.search([]),
            })
        else:
            _logger.info("nao CADASTRADO")
            return http.request.render('ud_ru.cadastro', {
                # 'grus': grus.search([]),
            })
        # obj_set = super(models.Model, self).create(vals)
        # usuario_ud_group = self.env.ref('ud.usuario_ud')
        # obj_set.groups_id |= usuario_ud_group
        # return obj_set

        # res = super(Responsavel, self).create(vals)
        # group_gerente_servico = self.env.ref('ud_almoxarifado.group_ud_almoxarifado_gerente')
        # res.pessoa_id.groups_id |= group_gerente_servico
        # return res

    @http.route('/ud_ru/almocar/', auth='public', website=True)
    def almocar(self, **kw):
        if kw.get('cpf'):
            _logger.info("############################# PESSOA")
            Pessoa = http.request.env['res.users']
            pessoa = Pessoa.search([('cpf', '=', kw.get('cpf'))])

            Refeicao_tipo = http.request.env['ud.ru.refeicao_tipo']
            refeicao_tipo = Refeicao_tipo.search([('name', '=', 'Almoço')])#,('ativo','=',True)

            valor_refeicao = 0

            _logger.info(pessoa.saldo)
            # _logger.info("refeicao_tipo.name")
            # _logger.info(refeicao_tipo.name)
            # _logger.info("bolsista")
            # _logger.info(pessoa.perfil_ids.bolsista)
            #
            # _logger.info("perfil_principal")
            # _logger.info(pessoa.perfil_principal)
            #ver o tipo de bolsa para fazer a comparação

            if len(pessoa.perfil_ids) > 1:
                perfil = pessoa.perfil_principal
                return "Almoçou - Tratar"
            else:
                perfil = pessoa.perfil_principal

            if perfil == "Discente":
                if (pessoa.perfil_ids.bolsista): #TODO MUDAR A CONDIÇÃO PARA COMPARAR O TIPO DE BOLSA
                    valor_refeicao = refeicao_tipo.valor_bolsista
                else:
                    valor_refeicao = refeicao_tipo.valor_aluno
            elif perfil == "Técnico":
                valor_refeicao = refeicao_tipo.valor_tecnico
            elif perfil == "Docente":
                valor_refeicao = refeicao_tipo.valor_docente

            if pessoa.saldo < valor_refeicao:
                return http.request.render('ud_ru.index', {
                    'msg_alerta': "Saldo insuficiente para {}. Saldo atual é {}.".format(pessoa.name, pessoa.saldo),
                })

            # refeicao_id = 0
            refeicao_id = http.request.env['ud.ru.refeicao'].create({#TODO VER O TIPO DE DADOS DE tipo_refeicao_id
                # 'name': refeicao_id,
                'valor': valor_refeicao,
                'tipo_refeicao_id': refeicao_tipo.id,
                'pessoa_id': pessoa.id,
            })
            _logger.info("refeicao_id")
            _logger.info(type(refeicao_id))
            _logger.info(refeicao_id)
            _logger.info(refeicao_id.id)
            movimentacao_id = http.request.env['ud.ru.movimentacao'].create({
                'codigo': "A_{}".format(refeicao_id.id),
                'valor': valor_refeicao,
                'tipo': "almoco",
                'pessoa_id': pessoa.id,
            })

            pessoa.decrementar_saldo(valor_refeicao)
            _logger.info(pessoa.saldo)

            # Refeicao_tipo = http.request.env['ud.ru.refeicao_tipo']
            # refeicao_tipo = Refeicao_tipo.search([()])
            # pessoa.decrementar_saldo(2)

            # _logger.info(pessoa.perfil_ids[0])
            # _logger.info(pessoa.perfil_ids.tipo_id)
            # _logger.info(type(pessoa.perfil_ids))
            # _logger.info(pessoa.perfil_principal)
            # _logger.info("############################# KW")
            # _logger.info(kw)
            _logger.info("#############################")
            return http.request.render('ud_ru.index', {
                'msg_ok': "Foi debitado R$ {} de {}.".format(valor_refeicao,pessoa.name),
            })
        else:
            return http.request.render('ud_ru.index')

        # return http.request.render('ud_ru.almocar', {
        #     'grus': grus.search([]),
        # })
        # return http.request.render('ud_biblioteca_website.publicacoes', context)

    # @http.route('/academy/<name>/', auth='public', website=True)
    # def teacher(self, name):
    #     return '<h1>{}</h1>'.format(name)

    # @http.route('/academy/<int:id>/', auth='public', website=True)
    # def teacher(self, id):
    #     return '<h1>{} ({})</h1>'.format(id, type(id).__name__)

#     @http.route('/ud_ru/ud_ru/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ud_ru.listing', {
#             'root': '/ud_ru/ud_ru',
#             'objects': http.request.env['ud_ru.ud_ru'].search([]),
#         })

#     @http.route('/ud_ru/ud_ru/objects/<model("ud_ru.ud_ru"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ud_ru.object', {
#             'object': obj
#         })
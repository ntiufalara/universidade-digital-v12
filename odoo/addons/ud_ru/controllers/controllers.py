# -*- coding: utf-8 -*-
from odoo import http

import logging

from odoo.exceptions import ValidationError
import json

_logger = logging.getLogger(__name__)

class UdRu(http.Controller):
    # @http.route('/ud_ru/ud_ru/', auth='user', website=True)
    # def index(self, **kw):
    #     return http.request.render('ud_ru.index', {  })


    @http.route('/cadastrar/', auth='public', methods=['get'], csrf=False)
    def index(self):
        return http.request.render('ud_ru.cadastro')

    @http.route('/cadastrar/', auth='public', methods=['post'], csrf=False)
    def process_cadastro(self, **kwargs):

        #verificar se usuário já existe - cpf unico?
        try:
            Users = http.request.env['res.users']
            # contato - ok
            # endereco?
            # perfil - criar a partir da matricula - ok
            # defenir a senha
            # permissoes apenas as necessárias

            obj_set = Users.sudo().create(kwargs)

            vinculo = http.request.env['ud.perfil.tipo'].sudo().search([('id', '=', kwargs.get('vinculo'))])
            Perfil = http.request.env['ud.perfil']
            perfil_id = Perfil.sudo().create({
                'tipo_id': vinculo.id,
                'curso_ou_setor': "curso",
                'matricula': kwargs.get('matricula'),
                'curso_id': kwargs.get('curso'),
                'pessoa_id': obj_set.id,
            })

            obj_set.perfil_ids |= perfil_id
            obj_set.groups_id |= http.request.env.ref('ud_ru.group_ud_ru_usuario')

        except ValidationError as e:
            _logger.info("---------------ERROR")
            _logger.info(str(e.args[0]))
            return http.request.render('ud_ru.cadastro', {
                'error': e.args[0]
            })
        return http.request.render('ud_ru.cadastro', {
            'success': True
        })



    @http.route('/ud_ru/transferir/', auth='public', methods=['get'])
    def transferir(self):
        return http.request.render('ud_ru.transferencia')

    @http.route('/ud_ru/transferir/', auth='public', methods=['post'])
    def process_transferir(self, **kwargs):

        try:#ver se será necessáro
            _logger.info("---------------TRANSFERENCIA")
            Pessoa = http.request.env['res.users']
            transferidor = Pessoa.search([('id', '=', http.request.env.uid)])
            valor_tranferencia = float(kwargs.get('valor'))

            # VALIDAR SALDO E PESQUISAR DESTINATÁRIO
            if (transferidor.saldo >= valor_tranferencia):
                destinatario = Pessoa.search([('cpf', '=', kwargs.get('cpf_destinatario'))])

                destinatario.incrementar_saldo(valor_tranferencia)
                transferidor.decrementar_saldo(valor_tranferencia)

                Transferencia = http.request.env['ud.ru.transferencia']
                transferencia_id = Transferencia.create({
                    'valor': kwargs.get('valor'),
                    'pessoa_id': transferidor.id,
                    'destinatario_id': destinatario.id,
                })

                # Movimentacao = http.request.env['ud.ru.movimentacao']
                # movimentacao1_id = Movimentacao.create({
                #     'codigo': "T_{}".format(transferencia_id.id),
                #     'valor': kwargs.get('valor'),
                #     'tipo': "trans_env",
                #     'pessoa_id': transferidor.id,
                # })
                # movimentacao2_id = Movimentacao.create({
                #     'codigo': "T_{}".format(transferencia_id.id),
                #     'valor': kwargs.get('valor'),
                #     'tipo': "trans_rec",
                #     'pessoa_id': destinatario.id,
                # })
            else:
                return http.request.render('ud_ru.transferencia', {
                    'error': "Não foi possível realizar a tranferência pois o saldo é inferior ao valor informado."
                })
        except ValidationError as e:
            return http.request.render('ud_ru.transferencia', {
                'error': e.args[0]
            })
        return http.request.render('ud_ru.transferencia', {
            'success': True,
            'msg_ok': "Transferência de {} realizada para {}.".format(kwargs.get('valor'), destinatario.name),
        })


    @http.route('/ud_ru/almocar/', auth='public', website=True)
    def almocar(self, **kw):
        if kw.get('cpf'):
            Pessoa = http.request.env['res.users']
            pessoa = Pessoa.search([('cpf', '=', kw.get('cpf'))])

            Refeicao_tipo = http.request.env['ud.ru.refeicao_tipo']
            refeicao_tipo = Refeicao_tipo.search([('name', '=', 'Almoço')])  # ,('ativo','=',True)

            valor_refeicao = 0

            # ver o tipo de bolsa para fazer a comparação
            # validar se já almoçou no dia

            # if len(pessoa.perfil_ids) > 1:
            #     perfil = pessoa.perfil_principal
            #     return "Almoçou - Tratar"
            # else:
            #     perfil = pessoa.perfil_principal
            perfil = pessoa.perfil_principal

            if perfil == "Discente":
                if (pessoa.perfil_ids.bolsista):  # TODO MUDAR A CONDIÇÃO PARA COMPARAR O TIPO DE BOLSA
                    valor_refeicao = refeicao_tipo.valor_bolsista
                else:
                    valor_refeicao = refeicao_tipo.valor_aluno
            elif perfil == "Técnico" or perfil == "Docente":
                valor_refeicao = refeicao_tipo.valor_servidor
            # elif perfil == "Docente":
            #     valor_refeicao = refeicao_tipo.valor_docente

            if pessoa.saldo < valor_refeicao:
                return http.request.render('ud_ru.index', {
                    'msg_alerta': "Saldo insuficiente para {}. Saldo atual é R$ {}.".format(pessoa.name, str(pessoa.saldo).replace('.',',')),
                })

            # refeicao_id = http.request.env['ud.ru.refeicao'].create({
            #     # 'name': refeicao_id,
            #     'valor': valor_refeicao,
            #     'tipo_refeicao_id': refeicao_tipo.name,
            #     'pessoa_id': pessoa.id,
            # })

            movimentacao_id = http.request.env['ud.ru.movimentacao'].create({
                # 'codigo': "A_{}".format(refeicao_id.id),
                'valor': valor_refeicao,
                'tipo': "almoco",
                'pessoa_id': pessoa.id,
                'funcionario_id': http.request.env.uid,
            })

            pessoa.decrementar_saldo(valor_refeicao)

            return http.request.render('ud_ru.index', {
                'msg_ok': "Foi debitado R$ {} de {}.".format(valor_refeicao, pessoa.name),
            })
        else:
            return http.request.render('ud_ru.index')


    @http.route('/ud_ru/get_uid/', auth='user', methods=['get'])  # , type="json"
    def get_id(self, **kwargs):
        _logger.info('GET UID:')
        _logger.info(kwargs)
        Pessoa = http.request.env['res.users']
        pessoa = Pessoa.search([('cpf', '=', kwargs.get('cpf'))])  #

        return json.dumps({"uid": pessoa.id})

    @http.route('/ud_ru/get_saldo/', auth='user', methods=['get'])  # , type="json"
    def get_saldo(self, **kwargs):
        _logger.info('GET SALDO:')
        _logger.info(kwargs)

        Pessoa = http.request.env['res.users']
        usuario = Pessoa.search([('cpf', '=', kwargs.get('cpf'))])  #
        # _logger.info(pessoa.name)
        return json.dumps({"saldo": usuario.saldo})

    @http.route('/ud_ru/get_extrato/', auth='user', methods=['get'])  # , type="json", auth='public',
    def get_extrato(self, **kwargs):
        # https://www.odoo.com/documentation/12.0/reference/orm.html
        Movimentacao = http.request.env['ud.ru.movimentacao']
        movimentacoes = Movimentacao.search(
            [('cpf', '=', kwargs.get('cpf'))])  #
        dados = []

        for movimentacao in movimentacoes:
            _logger.info(movimentacao.data_hora.date)
            mov = {
                "tipo": movimentacao.tipo,
                "data_hora": str(movimentacao.data_hora.strftime('%d/%m/%Y %H:%M')),
                "valor": movimentacao.valor,
            }
            dados.append(mov)

        return json.dumps(dados)  # json.dumps(dados)#

    @http.route('/ud_ru/get_nome/', auth='user', methods=['get'])
    def get_nome(self, id, **kwargs):
        Pessoa = http.request.env['res.users']

        pessoa = Pessoa.search([('cpf', '=', kwargs.get('cpf'))])  #

        return json.dumps({"nome": pessoa.name})


    # @http.route('/academy/<name>/', auth='public', website=True)
    # def teacher(self, name):
    #     return '<h1>{}</h1>'.format(name)

    # @http.route('/academy/<int:id>/', auth='public', website=True)
    # def teacher(self, id):
    #     return '<h1>{} ({})</h1>'.format(id, type(id).__name__)

    # @http.route('/ud_ru/ud_ru/objects/', auth='public')
    # def list(self, **kw):
    #     return http.request.render('ud_ru.listing', {
    #         'root': '/ud_ru/ud_ru',
    #         'objects': http.request.env['ud_ru.ud_ru'].search([]),
    #     })

#     @http.route('/ud_ru/ud_ru/objects/<model("ud_ru.ud_ru"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ud_ru.object', {
#             'object': obj
#         })

# class Utils(object):
#         @staticmethod
#         def validate_password(senha):
#             """
#             Validate password algorithm
#             """
#             if len(senha) < 8:
#                 raise ValueError(u"A senha precisa ter mais de %d digitos" % 8)
#             elif not re.search(r'[^\d]', senha) and re.search(r'\d', senha):
#                 raise ValueError(u'A senha precisa possuir números e letras')
#
#         @staticmethod
#         def validar_cpf(cpf):
#             """
#             Valida CPFs
#             """
#
#             def calcula_dv1(_cpf):
#                 start = 10
#                 cpf_list = [int(i) for i in _cpf]
#                 soma = 0
#                 for i in cpf_list[:-2]:
#                     val = i * start
#                     soma += val
#                     start -= 1
#                 resto = soma % 11
#                 _dv1 = 11 - resto
#                 if resto < 2:
#                     _dv1 = 0
#                 return _dv1


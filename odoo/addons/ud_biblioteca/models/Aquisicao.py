# encoding: UTF-8
import logging
from datetime import timedelta, date, datetime

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import pytz

_logger = logging.getLogger(__name__)


class Aquisicao(models.Model):
    """
    Nome: ud.biblioteca.aquisicao
    Descrição: Cadastro de aquisições do repositório institucional
    """
    _name = 'ud.biblioteca.aquisicao'

    # _order = "ano_pub desc"

    name = fields.Html(u'Título', required=True, sanitize=False)
  
    # autor_ids = fields.Many2many('ud.biblioteca.publicacao.autor', 'ud_biblioteca_publicacao_autores', 'pub_id',
    #                              'autor_id', u'Autores')
    autores = fields.Char(u'Autores', required=True)
    ano_pub = fields.Char(u'Ano de publicação', required=True)
    
    
   


    def name_get(self):
        """
        Com nomes muito grandes, mostra apenas uma versão resumida
        :return:
        """
        result = super(Aquisicao, self).name_get()
        result_list = []
        slice_len = 50
        for obj in result:
            obj_list = list(obj)
            if len(obj_list[1]) > slice_len:
                obj_list[1] = u'{}...'.format(obj_list[1][:slice_len])
            result_list.append(obj_list)
        return result_list


    



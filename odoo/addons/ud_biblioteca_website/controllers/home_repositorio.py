import locale
from odoo import http


class HomeRepositorio(http.Controller):
    @http.route('/repositorio/', auth='public')
    def index(self, **kwargs):
        Cursos = http.request.env['ud.curso']
        Pc = http.request.env['ud.biblioteca.p_chave']
        Publicacao = http.request.env['ud.biblioteca.publicacao']
        Polo = http.request.env['ud.polo']

        cursos_arapiraca = Cursos.search(
            [('polo_id.campus_id.name', 'ilike', 'arapiraca'),
             ('publicacao_ids', '!=', None)],
            order='name asc'
        )
        ultimas_publicacoes = Publicacao.search([], order='create_date desc', limit=6)

        locale.setlocale(locale.LC_ALL, '')

        return http.request.render('ud_biblioteca_website.home_repositorio', {
            'cursos': cursos_arapiraca,
            'assuntos_count': locale.format_string('%d', Pc.search_count([]), grouping=True),
            'publicacoes_count': locale.format_string('%d', Publicacao.search_count([]), grouping=True),
            'unidades_count': Polo.search_count([]),
            'visualizacoes_count': locale.format_string('%d', Publicacao.visualizacoes_totais(), grouping=True),
            'ultimas_publicacoes': ultimas_publicacoes,
        })

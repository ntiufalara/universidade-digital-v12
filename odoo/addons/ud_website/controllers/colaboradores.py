from odoo import http


class Colaboradores(http.Controller):
    @http.route('/colaboradores/', auth='public')
    def index(self):
        Colaborador = http.request.env['ud_website.colaborador']
        Sobre = http.request.env['ud_website.sobre']

        colaboradores = Colaborador.sudo().search([], order='name')
        sobre = Sobre.sudo().search([], limit=1)
        return http.request.render('ud_website.colaboradores', {
            'colaboradores': colaboradores,
            'sobre': sobre,
        })

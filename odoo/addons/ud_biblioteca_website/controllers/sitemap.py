from odoo import http
import datetime


class Sitemap(http.Controller):
    @http.route('/sitemap.xml', auth='public')
    def index(self, **kwargs):
        Publicacao = http.request.env['ud.biblioteca.publicacao']
        pub_ids = Publicacao.sudo().search_read([], fields=['id', 'write_date'])
        return http.request.render('ud_biblioteca_website.sitemap_xml', {
            'date': datetime.date.today(),
            'pubs': pub_ids,
        }, content_type="text/xml")

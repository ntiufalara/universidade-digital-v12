import html2text

from odoo import models, fields, api


class Publicacao(models.Model):
    _name = 'ud.biblioteca.publicacao'
    _inherit = 'ud.biblioteca.publicacao'

    name_text = fields.Char('Nome (Somente texto)', compute="get_name_text")
    data_defesa_iso = fields.Char('Data de defesa no formato ISO', compute="get_data_defesa_iso")
    resumo_text = fields.Text('Resumo txt', compute="get_resumo_text")
    abstract_text = fields.Text('Resumo txt', compute="get_abstract_text")
    tags_xmllang = fields.Text('Tags com XML:LANG', compute="get_tags")
    keywords_text = fields.Text('Keywords', compute='get_keywords')

    @api.one
    def get_name_text(self):
        self.name_text = html2text.html2text(self.name).strip().replace('\n', ' ').replace('"', '&quot;').replace(
            '\'', '&apos;')

    @api.one
    def get_data_defesa_iso(self):
        if self.data_defesa:
            self.data_defesa_iso = self.data_defesa.strftime('%Y/%m/%d')
        else:
            self.data_defesa_iso = self.create_date.strftime('%Y/%m/%d')

    @api.one
    def get_tags(self):
        tags = ''
        # Abstract
        tags += '<meta name="DCTERMS.abstract" content="{}" xml:lang="pt_BR" />'.format(self.resumo_text)
        # Publisher
        company = self.env['res.company'].search([('id', '=', 1)])
        tags += '<meta name="DC.publisher" content="{}" xml:lang="pt_BR" />'.format(company.name)
        tags += '<meta name="DC.publisher" content="{}" xml:lang="pt_BR" />'.format(self.curso_id.name)
        tags += '<meta name="citation_publisher" content="{}" />'.format(company.name)
        # Subjects
        for p in self.palavras_chave_ids:
            tags += '<meta name="DC.subject" content="{}" xml:lang="pt_BR" />'.format(p.name)
        # Titulo
        tags += '<meta name="DC.title" content="{}" xml:lang="pt_BR" />'.format(self.name_text)
        tags += '<meta name="DC.type" content="{}" xml:lang="pt_BR" />'.format(self.tipo_id.name)
        tags += '<meta name="DC.description" content="{}" xml:lang="pt_BR" />'.format(self.resumo_text)
        self.tags_xmllang = tags

    @api.one
    def get_keywords(self):
        keywords = ''
        for i in range(len(self.palavras_chave_ids)):
            keywords += self.palavras_chave_ids[i].name
            if i != len(self.palavras_chave_ids) - 1:
                keywords += ', '
        self.keywords_text = keywords

    @api.one
    def get_resumo_text(self):
        self.resumo_text = html2text.html2text(self.resumo) if self.resumo else ''
        self.resumo_text = self.resumo_text.strip().replace('\n', ' ')

    @api.one
    def get_abstract_text(self):
        self.abstract_text = html2text.html2text(self.abstract) if self.abstract else ''
        self.abstract_text = self.abstract_text.strip().replace('\n', ' ')




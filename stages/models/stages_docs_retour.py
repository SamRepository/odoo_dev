# -*- coding: utf-8 -*-

from odoo import models, fields, api,  _

class StagesDocsRetour(models.Model):
    _name = 'stages.docs_retour'
    _description = 'Documents de Retour'
    _rec_name = 'name'

    name = fields.Char(string="Intitulé", required=True)
    type = fields.Selection(string="Type", selection=[('rapport', 'Rapport de stage visé'), ('ordre', 'Ordre de mission visé'), ], required=True, )
    piece_joint = fields.Binary(string="Piece joint",  )

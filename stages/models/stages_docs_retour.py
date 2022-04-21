# -*- coding: utf-8 -*-

from odoo import models, fields, api,  _

class StagesDocsRetour(models.Model):
    _name = 'stages.docs_retour'
    _description = 'Documents de Retour - وثائق الرجوع'
    _rec_name = 'name'

    name = fields.Char(string="Intitulé - إسم الوثيقة", required=True)
    type = fields.Selection(string="Type - نوع الوثيقة", selection=[('rapport', 'Rapport de stage visé'), ('ordre', 'Ordre de mission visé'), ('resultat ', 'Résultats Scientifiques'),], required=True, )
    piece_joint = fields.Binary(string="Piece joint - ملحقة الوثيقة", attachment=True)
    candidature_id = fields.Many2one(comodel_name="stages.candidature", string="Candidature Stage - طلب الترشح", required=True, )
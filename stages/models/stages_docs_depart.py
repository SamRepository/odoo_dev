# -*- coding: utf-8 -*-

from odoo import models, fields, api,  _

class StagesDocsDepart(models.Model):
    _name = 'stages.docs_depart'
    _description = 'Documents de Départ - وثائق الذهاب'
    _rec_name = 'name'

    name = fields.Char(string="Intitulé - إسم الوثيقة", required=True)
    type = fields.Selection(string="Type - نوع الوثيقة", selection=[('Project', 'Projet de travail - مشروع العمل'), ], required=True, )
    piece_joint = fields.Binary(string="Piece joint - ملحقة الوثيقة", attachment=True)
    candidature_id = new_field_id = fields.Many2one(comodel_name="stages.candidature", string="Candidature Stage - طلب الترشح", required=False, )

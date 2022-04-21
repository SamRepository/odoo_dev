# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class StagesDocsDepart(models.Model):
    _name = 'stages.docs_depart'
    _description = 'Documents de Départ - وثائق الذهاب'

    name = fields.Char(string="Intitulé - إسم الوثيقة", required=True)
    type = fields.Selection(string="Type - نوع الوثيقة",
                            selection=[('projet', 'Projet de travail'), ('objectifs', 'Objectifs du stage'),
                                       ('methodologie', 'Méthodologie'), ('impacts', 'Impacts attendus'), ],
                            required=True, )
    piece_joint = fields.Binary(string="Piece joint - ملحقة الوثيقة", attachment=True)
    candidature_perfec_id = fields.Many2one("stages.candidature.perfectionnement",
                                            string="Candidature Stage - طلب الترشح", )
    candidature_manif_id = fields.Many2one("stages.candidature.manifestation",
                                           string="Candidature Stage - طلب الترشح", )
    candidature_sejour_id = fields.Many2one("stages.candidature.sejour", string="Candidature Stage - طلب الترشح", )

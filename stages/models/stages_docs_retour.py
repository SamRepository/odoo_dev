# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class StagesDocsRetour(models.Model):
    _name = 'stages.docs_retour'
    _description = 'Documents de Retour - وثائق الرجوع'

    name = fields.Char(string="Intitulé - إسم الوثيقة", required=True)
    type = fields.Selection(string="Type - نوع الوثيقة",
                            selection=[('rapport', 'Rapport de stage visé'), ('ordre', 'Ordre de mission visé'),
                                       ('resultat ', 'Résultats Scientifiques'), ], required=True, )
    piece_joint = fields.Binary(string="Piece joint - ملحقة الوثيقة", attachment=True)
    candidature_perfec_id = fields.Many2one("stages.candidature.perfectionnement",
                                            string="Candidature Stage - طلب الترشح", )
    candidature_manif_id = fields.Many2one("stages.candidature.manifestation",
                                           string="Candidature Stage - طلب الترشح", )
    candidature_sejour_id = fields.Many2one("stages.candidature.sejour", string="Candidature Stage - طلب الترشح", )

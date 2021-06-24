# -*- coding: utf-8 -*-

from odoo import models, fields, api,  _

class StagesSession(models.Model):
    _inherit = ['event.event']
    # _name = 'stages.session'
    # _description = 'Session Stages - فترات التربص'
    # _rec_name = 'name'

    # name = fields.Char(string="Intitulé - إسم الفترة", required=True)
    # exercice_id= fields.Many2one(comodel_name="stages.exercice", required=True, string="Excersice Fiscal - السنة المالية")
    # date_debut = fields.Date(string="Date debut - تاريخ البداية", required=True, )
    # date_fin = fields.Date(string="Date fin - تاريخ النهاية", required=True, )
# -*- coding: utf-8 -*-

from odoo import models, fields, api,  _

class StagesChangePeriode(models.Model):
    _name = 'stages.change_periode'
    _description = 'Changement du Période - تغيير الفترة'

    cause = fields.Char(string="Cause - السبب", required=True)
    date_debut = fields.Date(string="Nouvelle date debut - تاريخ البداية الجديد", required=True, )
    date_fin = fields.Date(string="Nouvelle date fin - تاريخ النهاية الجديد", required=True, )

# -*- coding: utf-8 -*-

from odoo import models, fields, api,  _

class StagesChangePeriode(models.Model):
    _name = 'stages.change_periode'
    _description = 'Changement du Période'

    cause = fields.Char(string="Cause", required=True)
    date_debut = fields.Date(string="Nouvelle date debut", required=True, )
    date_fin = fields.Date(string="Nouvelle date fin", required=True, )

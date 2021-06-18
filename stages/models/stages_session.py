# -*- coding: utf-8 -*-

from odoo import models, fields, api,  _

class StagesSession(models.Model):
    _name = 'stages.session'
    _description = 'Session Stages'
    _rec_name = 'name'

    name = fields.Char(string="Intitulé", required=True)
    exercice_id= fields.Many2one(comodel_name="stages.exercice", string="Exercice Fiscal", required=True, )
    date_debut = fields.Date(string="Date debut", required=True, )
    date_fin = fields.Date(string="Date fin", required=True, )
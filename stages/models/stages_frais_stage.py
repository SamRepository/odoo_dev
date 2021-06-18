# -*- coding: utf-8 -*-

from odoo import models, fields, api,  _

class StagesFraisStage(models.Model):
    _name = 'stages.frais_stages'
    _description = 'Frais Stage'
    _rec_name = 'name'

    name = fields.Char(string="Intitulé", required=True)
    type = fields.Selection(string="Type", selection=[('visa', 'Visa'), ('assurance', 'Assurance'), ('inscription', 'Inscription'),('transport', 'Transport'),], required=True, )
    montant = fields.Float(string="Montant",  required=True, )
    piece_joint = fields.Binary(string="Piece joint", )
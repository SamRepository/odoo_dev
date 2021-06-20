# -*- coding: utf-8 -*-

from odoo import models, fields, api,  _

class StagesFraisStage(models.Model):
    _name = 'stages.frais_stages'
    _description = 'Frais Stage - تكاليف الترص'
    _rec_name = 'name'

    name = fields.Char(string="Intitulé - إسم التكلفة", required=True)
    type = fields.Selection(string="Type - نوع التكلفة", selection=[('visa', 'Visa'), ('assurance', 'Assurance'), ('inscription', 'Inscription'),('transport', 'Transport'),], required=True, )
    montant = fields.Float(string="Montant - قيمة التكلفة",  required=True, )
    piece_joint = fields.Binary(string="Piece joint - الوثيقة", attachment=True)
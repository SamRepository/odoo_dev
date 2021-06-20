# -*- coding: utf-8 -*-

from odoo import models, fields, api,  _

class StagesGrade(models.Model):
    _name = 'stages.grade'
    _description = 'Grades'
    _rec_name = 'name'

    name = fields.Char(string="Intitulé", required=True)
    categories = fields.Char(string="Catégories", required=False)
    corps = fields.Char(string="Corps", required=False)


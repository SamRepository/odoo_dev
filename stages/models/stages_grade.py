# -*- coding: utf-8 -*-

from odoo import models, fields, api,  _

class StagesGrade(models.Model):
    _name = 'stages.grade'
    _description = 'Grade Scientifique - الرتب العلمية'
    _rec_name = 'name'

    name = fields.Char(string="Intitulé grade - إسم الرتبة", required=True)
    categories = fields.Char(string="Catégories - الفئة", required=False)
    corps = fields.Char(string="Corps - السلك", required=False)


from odoo import models, fields, api, _


class PfeGrade(models.Model):
    _name = 'pfe.grade'
    _description = 'Grade Scientifique - الرتب العلمية'
    _rec_name = 'name'

    name = fields.Char(string="Intitulé grade", required=True)
    intitule_grade_ar = fields.Char(string="Intitulé grade ar", required=True)
    categories = fields.Char(string="Catégories", required=False)
    corps = fields.Char(string="Corps", required=False)
    indice_min = fields.Integer(string="Indice minimal", required=False)
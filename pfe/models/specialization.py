from odoo import models, fields
class Specialization(models.Model):
    _name = 'pfe.specialization'
    _description = 'Specialization'

    name = fields.Char(string="Specialization", required=True)
    education_level_ids = fields.Many2many(
        'pfe.education_level',
        'education_specialization_rel',
        'specialization_id',
        'education_level_id',
        string="Education Levels"
    )
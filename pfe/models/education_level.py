from odoo import models, fields
class EducationLevel(models.Model):
    _name = 'pfe.education_level'
    _description = 'Education Level'
    duration = fields.Integer(string="Duration (Years)", required=True, help="Number of years for this education level")
    name = fields.Char(string="Level", required=True)
    specialization_ids = fields.Many2many(
        'pfe.specialization',
        'education_specialization_rel',
        'education_level_id',
        'specialization_id',
        string="Specializations"
    )
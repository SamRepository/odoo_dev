from odoo import models, fields, api

class Student(models.Model):
    _inherit = 'hr.employee'

    is_student = fields.Boolean(string='Is Student', default=True)
    avg_grade = fields.Float(string='Average Grade')

    specialization_id = fields.Many2one(
        'pfe.specialization', string='Specialization Study',
        related='group_id.specialization_id', store=True, readonly=False
    )

    education_level_id = fields.Many2one(
        'pfe.education_level', string='Education Level',
        related='group_id.education_level_id', store=True, readonly=False
    )

    group_id = fields.Many2one(
        'pfe.sgroupe',
        string='Student Group',
        ondelete='set null'
    )

    is_student_in_group = fields.Boolean(
        string="Is in Group",
        compute="_compute_is_student_in_group",
        store=True
    )



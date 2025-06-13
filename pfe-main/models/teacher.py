from odoo import models, fields

class Teacher(models.Model):
    _inherit = 'hr.employee'
    teacher_tag = fields.Boolean(string="Is Teacher", default=False)

    civility = fields.Selection([
        ('mr', 'Mr.'),
        ('mrs', 'Mrs.'),
        ('ms', 'Ms.')
    ], string="Civility", required=True)

    specialty = fields.Selection([
        ('math', 'Mathematics'),
        ('cs', 'Computer Science'),
        ('physics', 'Physics'),
        ('other', 'Other')
    ], string="Specialty")
    category_ids = fields.Many2many(
        'hr.employee.category',

        string="Categories"
    )

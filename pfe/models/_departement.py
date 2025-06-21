from odoo import models, fields

class Department(models.Model):
    _inherit = 'hr.department'

    intitule_dep_ar = fields.Char(string='Intitulé dep Ar - اسم القسم بالعربية')

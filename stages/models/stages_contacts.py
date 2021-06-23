from odoo import models, fields, api,  _

class StagesContacts(models.Model):
     _inherit = ['res.partner']

     grade_acc = fields.Char(string='Grade accueillant - الرتبة العلمية للمستقبل')
from odoo import models, fields, api,  _

class StagesLaboratoire(models.Model):
     _inherit = ['res.partner']

    # _name = 'stages.laboratoire'
    # _description = 'Laboratoire - المخابر'
    # _rec_name = 'name'
    #
    # name = fields.Char(string='Nom du laboratoire - إسم المخبر', required=True)
    # member_ids = fields.One2many('stages.enseignant', 'lab_id', string='Members - الاعضاء', readonly=True)
from odoo import models, fields, api,  _

class StagesDepartement(models.Model):
    _name = 'stages.departement'
    _description = 'Département - الاقسام'
    _rec_name = 'name'

    name = fields.Char(string='Nom du département - إسم القسم', required=True)
    chef_dpte_id = fields.Many2one('stages.enseignant', string='Chef de département - رئيس القسم', )
    member_ids = fields.One2many('stages.enseignant', 'dpte_id', string='Members - الأساتذة', readonly=True)

from odoo import models, fields, api,  _

class StagesConseil(models.Model):
    _name = 'stages.conseil'
    _description = 'Conseil Scientifique'
    _rec_name = 'name'

    name = fields.Char(string="Référence", required=True)
    date_pv = fields.Date(string="Date du Conseil", required=True, )
    president = fields.Char(string="Président", required=False,)
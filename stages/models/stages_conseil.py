from odoo import models, fields, api,  _

class StagesConseil(models.Model):
    _name = 'stages.conseil'
    _description = 'Conseil Scientifique - المجلس العلمي'
    _rec_name = 'name'

    name = fields.Char(string="Référence - المرجع", required=True)
    date_pv = fields.Date(string="Date du Conseil - تاريخ الانعقاد", required=True, )
    president = fields.Char(string="Président - رئيس المجلس", required=False, default='Boudjadaar Djamel')
from odoo import models, fields, api,  _

class StagesConseil(models.Model):
    _name = 'stages.conseil'
    _description = 'Conseil Scientifique - المجلس العلمي'
    _rec_name = 'name'

    name = fields.Char(string="Référence - المرجع", required=True)
    date_pv = fields.Date(string="Date du Conseil - تاريخ الانعقاد", required=True, )
    session_id = fields.Many2one(comodel_name="stages.session", string="Session - االفترة", required=False, )
    president_id = fields.Many2one(comodel_name="hr.employee", string="Président - رئيس المجلس", required=False, )
    memeber_ids = fields.One2many(comodel_name="stages.conseil.members", inverse_name="member_id", string="Members - اعضاء المجلس", required=False, )

class StagesConseilMembers(models.Model):
    _name = 'stages.conseil.members'
    _description = 'Members - اعضاء المجلس'

    conseil_id= fields.Many2one(comodel_name="stages.conseil", string= "Conseil Scientifique - المجلس العلمي",)
    member_id = fields.Many2one(comodel_name="hr.employee", string="Membre -  العضو",)








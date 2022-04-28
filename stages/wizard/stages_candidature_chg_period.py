from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError


class ChangePeriodWizard(models.TransientModel):
    _name = 'stages.candidature.chg.period'
    _description = 'Changer Période Candidature'


    date_depart = fields.Date(string="Date de départ", required=True, )
    date_retour = fields.Date(string="Date de retour ", required=True, )
    cause_chg_period = fields.Char(string="Cause changement période", required=False, )

    def action_confirm(self):
       return

    # duree = fields.Integer(string="Durée", compute='set_durre', store=True, )
    # cause_chg_period = fields.Char(string="Cause changement période", required=False, )
    # currency_id = fields.Many2one('res.currency',default=lambda self: self.env['res.currency'].search([('name', '=', 'DZD')]).id, readonly=True)
    # montant = fields.Float(string="Montant", compute="set_montant", )

    # @api.depends('date_depart', 'date_retour')
    # def set_durre(self):
    #     for rec in self:
    #         if rec.date_depart:
    #             if rec.date_retour:
    #                 if rec.date_retour > rec.date_depart:
    #                     rec.duree = (rec.date_retour - rec.date_depart).days
    #                 else:
    #                     raise UserError('La date de retour doit être supérieure à la date de départ')


    # @api.depends('type_stage_id', 'zone', 'duree')
    # def set_montant(self):
    #     for rec in self:
    #         if rec.type_stage_id:
    #             obj = self.env['stages.type_stage.indemnite'].search(
    #             [('type_stage_id', '=', rec.type_stage_id.name), ('zone_id.name', '=', rec.zone),
    #              ('nombre_jour', '=', rec.duree)])
    #             rec.montant = obj.montant
    #         else:
    #             rec.montant = "Montant non ecnore calculé"
    #
    #
    # def action_confirm(self):
    #     for rec in self:
    #         rec.state = 'confirm'
    #
    # def action_cancel(self):
    #     for rec in self:
    #         rec.state = 'cancel'

    # def _default_country_id(self):
    #     return self.env.ref('base.DZD').id


# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
#
# Copyright (c) 2016  - Osis - www.osis-dz.net


from odoo import fields, models


class AccountConfigSettings(models.TransientModel):
    _inherit = 'account.config.settings'

    hours = fields.Float(related='company_id.hours', string='Nombre Heures *')
    days = fields.Integer(related='company_id.days', string='Nombre Jours *')
    leave = fields.Float(related='company_id.leave', string='Cumul conge / Mois *')
    director_id = fields.Many2one('hr.employee', related='company_id.director_id',
                                  string='DG *')
    imm_ss = fields.Char(related='company_id.imm_ss', string='Immatriculation sociale *')

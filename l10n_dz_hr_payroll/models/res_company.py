# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
#
# Copyright (c) 2016  - Osis - www.osis-dz.net

from odoo import fields, models
from odoo.addons import decimal_precision as dp

class ResCompany(models.Model):
    _inherit = 'res.company'

    hours = fields.Float(string='Nombre Heures', digits=dp.get_precision('Payroll'))
    days = fields.Integer(string='Nombre Jours')
    leave = fields.Float(string='Cumul conge / Mois', digits=dp.get_precision('Payroll'))
    director_id = fields.Many2one('hr.employee', string='DG', default=1)
    imm_ss = fields.Char(string='immatriculation sociale')





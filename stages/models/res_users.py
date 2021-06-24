# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, models, fields

class User(models.Model):
    _inherit = ['res.users']

    # enseignant_ids = fields.One2many('stages.enseignant', 'user_id', string='Enseignants Concernés - الاساتذة المعنيين')
    #
    # @api.multi
    # def write(self, vals):
    #     """ Synchronize user and its related enseignant """
    #     result = super(User, self).write(vals)
    #     enseignant_values = {}
    #     for fname in [f for f in ['name', 'email', 'image', 'tz'] if f in vals]:
    #         enseignant_values[fname] = vals[fname]
    #     if enseignant_values:
    #         self.env['stages.enseignant'].sudo().search([('user_id', 'in', self.ids)]).write(enseignant_values)
    #     return result
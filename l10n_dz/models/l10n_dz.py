# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
#
# Copyright (c) 2016  - Osis - www.osis-dz.net

from odoo import fields, models

class ResCompany(models.Model):
    _inherit = 'res.company'

    rc = fields.Char(string='R.C')
    nif = fields.Char(string='N.I.F', size=15)
    nis = fields.Char(string='N.I.S')
    ai = fields.Char(string='Article d\'imposition')
    code_activite = fields.Char(string='Code d\'activité')
    activite = fields.Char(string='Activité')
    impot_dir = fields.Many2one('res.country.state', string='Direction des impôrts')
    impot_rec = fields.Char(string='Recette des impôts de')
    impot_com = fields.Many2one('res.commune', string='Commune de')


class ResPartner(models.Model):
    _inherit = 'res.partner'

    rc = fields.Char(string='R.C')
    nif = fields.Char(string='N.I.F', size=15)
    nis = fields.Char(string='N.I.S')
    ai = fields.Char(string='Article d\'imposition')

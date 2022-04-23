# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
#
# Copyright (c) 2022  - samir.sellami@live.fr

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

import re

PATTERN_NIS_NIF = "^[a-zA-Z0-9]{15}$"
PATTERN_AI = "^[a-zA-Z0-9]{11}$"

class ResPartner(models.Model):
    _inherit = 'res.partner'

    rc = fields.Char(string="N° RC", help="Numéro du registre de commerce",)
    nis = fields.Char(string="NIS",size=15,help="Numéro d'Identification Statistique",)
    nif = fields.Char(string="NIF", size=15, help="Numéro d’Identification Fiscal",)
    ai = fields.Char(string="AI", size=11, help="Numéro d'article d'imposition",)

    def valid_pattern(self, pattern, field, msg):
        if field and not re.match(pattern, field):
            raise ValidationError(msg)

    @api.constrains('nis')
    def is_valid_nis(self):
        for record in self:
            record.valid_pattern(PATTERN_NIS_NIF, record.nis, "NIS invalide.")

    @api.constrains('nif')
    def is_valid_nif(self):
        for record in self:
            record.valid_pattern(PATTERN_NIS_NIF, record.nif, "NIF invalide.")

    @api.constrains('ai')
    def is_valid_ai(self):
        for record in self:
            record.valid_pattern(PATTERN_AI, record.ai, "AI invalide.")

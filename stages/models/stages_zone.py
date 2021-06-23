# -*- coding: utf-8 -*-

from odoo import models, fields, api,  _

class StagesZone(models.Model):
    _inherit = ['res.country.group']


    indemnite_jour = fields.Float(string="Indémnite Jour - علاوة المنطقة",  required=False, )
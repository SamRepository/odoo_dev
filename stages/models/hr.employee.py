# -*- coding: utf-8 -*-

from odoo import models, fields, api,  _

class Employee(models.Model):
    _inherit = ['hr.employee']
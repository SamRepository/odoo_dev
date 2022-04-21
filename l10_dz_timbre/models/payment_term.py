# -*- encoding: utf-8 -*-

from odoo import fields, models, api

class AccountPaymentTerm(models.Model):
    _inherit = 'account.payment.term'

    payment_type = fields.Selection([('cash','Cash'),
                                     ('nocash','Other'),
                                     ],'Type', required=True, default='nocash')




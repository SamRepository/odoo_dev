# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
#
# Copyright (c) 2019

from odoo import fields, models, api,_




class PurchaseOrderr(models.Model):
    _inherit = "purchase.order"

    @api.one
    @api.depends('payment_term_id','amount_total')
    def _amount_timbre(self):
        for order in self:
            amount_timbre = order.amount_untaxed + order.amount_tax
            if order.payment_term_id and order.payment_term_id.payment_type == 'cash':
                timbre = self.env['config.timbre']._timbre(order.amount_untaxed + order.amount_tax)
                self.timbre = timbre['timbre']


    @api.onchange('payment_term_id')
    def onchange_payment_term(self):
        if not self.payment_term_id:
            self.update({
                'payment_type': False,
            })
            return
        values = {
            'payment_type': self.payment_term_id and self.payment_term_id.payment_type or False,
        }
        self.update(values)

    # inherited method from purchase order model
    @api.depends('order_line.price_total','payment_term_id')
    def _amount_all(self):
        for order in self:
            amount_untaxed = amount_tax = 0.0
            for line in order.order_line:
                amount_untaxed += line.price_subtotal
                # FORWARDPORT UP TO 10.0
                if order.company_id.tax_calculation_rounding_method == 'round_globally':
                    taxes = line.taxes_id.compute_all(line.price_unit, line.order_id.currency_id, line.product_qty, product=line.product_id, partner=line.order_id.partner_id)
                    amount_tax += sum(t.get('amount', 0.0) for t in taxes.get('taxes', []))
                else:
                    amount_tax += line.price_tax
            order.update({
                'amount_untaxed': order.currency_id.round(amount_untaxed),
                'amount_tax': order.currency_id.round(amount_tax),
                'amount_total': amount_untaxed + amount_tax,
            })
            amount_timbre = order.amount_total 
            if (order.payment_term_id and order.payment_term_id.payment_type == 'cash'):
                timbre = self.env['config.timbre']._timbre(amount_timbre)
                self.timbre = timbre['timbre'] 
                self.amount_total = timbre['amount_timbre']

    payment_type = fields.Char('Type de paiement')
    timbre = fields.Monetary(string='Timbre', store=True, readonly=True,
                             compute='_amount_timbre', track_visibility='onchange')

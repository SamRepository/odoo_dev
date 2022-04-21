# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
#
# Copyright (c) 2019


from odoo import fields, models, api,_



class AccountInnvoice(models.Model):
    _inherit = "account.invoice"



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


    # inherited method from account invoice model
    @api.one
    @api.depends('payment_term_id','invoice_line_ids.price_subtotal', 'tax_line_ids.amount', 'currency_id', 'company_id', 'type')
    def _compute_amount(self):
        round_curr = self.currency_id.round
        self.amount_untaxed = sum(line.price_subtotal for line in self.invoice_line_ids)
        self.amount_tax = sum(round_curr(line.amount) for line in self.tax_line_ids)
        self.amount_total = self.amount_untaxed + self.amount_tax
        for order in self:
            amount_timbre = order.amount_total 
            if (order.payment_term_id and order.payment_term_id.payment_type == 'cash'):
                timbre = self.env['config.timbre']._timbre(amount_timbre)
                self.timbre = timbre['timbre'] 
                self.amount_total = timbre['amount_timbre']
        amount_total_company_signed = self.amount_total
        amount_untaxed_signed = self.amount_untaxed
        if self.currency_id and self.company_id and self.currency_id != self.company_id.currency_id:
            currency_id = self.currency_id.with_context(date=self.date_invoice)
            amount_total_company_signed = currency_id.compute(self.amount_total, self.company_id.currency_id)
            amount_untaxed_signed = currency_id.compute(self.amount_untaxed, self.company_id.currency_id)
        sign = self.type in ['in_refund', 'out_refund'] and -1 or 1
        self.amount_total_company_signed = amount_total_company_signed * sign
        self.amount_total_signed = self.amount_total * sign
        self.amount_untaxed_signed = amount_untaxed_signed * sign



    payment_type = fields.Char('Type de paiement')
    timbre = fields.Monetary(string='Timbre', store=True, readonly=True,
                             compute='_amount_timbre', track_visibility='onchange')


    # Creates invoice related analytics and financial move lines
    @api.multi
    def action_move_create(self):
        account_move = self.env['account.move']

        for inv in self:
            if not inv.journal_id.sequence_id:
                raise UserError(_('Please define sequence on the journal related to this invoice.'))
            if not inv.invoice_line_ids:
                raise UserError(_('Please create some invoice lines.'))
            if inv.move_id:
                continue

            ctx = dict(self._context, lang=inv.partner_id.lang)

            if not inv.date_invoice:
                inv.with_context(ctx).write({'date_invoice': fields.Date.context_today(self)})
            company_currency = inv.company_id.currency_id

            iml = inv.invoice_line_move_line_get()
            iml += inv.tax_line_move_line_get()
            # create timbre line in account move line
            iml += inv.timbre_line_move_line_get()

            diff_currency = inv.currency_id != company_currency
            total, total_currency, iml = inv.with_context(ctx).compute_invoice_totals(company_currency, iml)

            name = inv.name or '/'
            if inv.payment_term_id:
                totlines = inv.with_context(ctx).payment_term_id.with_context(currency_id=company_currency.id).compute(total, inv.date_invoice)[0]
                res_amount_currency = total_currency
                ctx['date'] = inv._get_currency_rate_date()
                for i, t in enumerate(totlines):
                    if inv.currency_id != company_currency:
                        amount_currency = company_currency.with_context(ctx).compute(t[1], inv.currency_id)
                    else:
                        amount_currency = False

                    # last line: add the diff
                    res_amount_currency -= amount_currency or 0
                    if i + 1 == len(totlines):
                        amount_currency += res_amount_currency

                    iml.append({
                        'type': 'dest',
                        'name': name,
                        'price': t[1],
                        'account_id': inv.account_id.id,
                        'date_maturity': t[0],
                        'amount_currency': diff_currency and amount_currency,
                        'currency_id': diff_currency and inv.currency_id.id,
                        'invoice_id': inv.id
                    })
            else:
                iml.append({
                    'type': 'dest',
                    'name': name,
                    'price': total,
                    'account_id': inv.account_id.id,
                    'date_maturity': inv.date_due,
                    'amount_currency': diff_currency and total_currency,
                    'currency_id': diff_currency and inv.currency_id.id,
                    'invoice_id': inv.id
                })
            part = self.env['res.partner']._find_accounting_partner(inv.partner_id)
            line = [(0, 0, self.line_get_convert(l, part.id)) for l in iml]
            line = inv.group_lines(iml, line)

            journal = inv.journal_id.with_context(ctx)
            line = inv.finalize_invoice_move_lines(line)

            date = inv.date or inv.date_invoice
            move_vals = {
                'ref': inv.reference,
                'line_ids': line,
                'journal_id': journal.id,
                'date': date,
                'narration': inv.comment,
            }
            ctx['company_id'] = inv.company_id.id
            ctx['invoice'] = inv
            ctx_nolang = ctx.copy()
            ctx_nolang.pop('lang', None)
            move = account_move.with_context(ctx_nolang).create(move_vals)
            # Pass invoice in context in method post: used if you want to get the same
            # account move reference when creating the same invoice after a cancelled one:
            move.post()
            # make the invoice point to that move
            vals = {
                'move_id': move.id,
                'date': date,
                'move_name': move.name,
            }
            inv.with_context(ctx).write(vals)
        return True

    # create timbre line in account move line
    @api.model
    def timbre_line_move_line_get(self):
        res = []
        timbre_account = self.env['config.timbre'].search([('name','=','Calcul Timbre')]).account_id.id
        if not timbre_account and self.payment_term_id.payment_type ==  'cash':
            raise ValidationError("Compte De Droit d’enregistrement n'est pas paramétré. \n Allez dans Comptabilité/Configuration/Comptablité/Configuration Timbre")
        for record in self:
            if record.timbre and record.payment_term_id and record.payment_term_id.payment_type == 'cash':

                res.append({
                    'type': 'tax',
                    'name': 'Timbre',
                    'price_unit': self.timbre,
                    'quantity': 1,
                    'price': self.timbre,
                    'account_id': timbre_account,
                    #'account_analytic_id': tax_line.account_analytic_id.id,
                    'invoice_id': self.id,
                })
        return res

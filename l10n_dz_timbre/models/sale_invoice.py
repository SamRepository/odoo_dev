# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
#
# Copyright (c) 2022  - samir.sellami@live.fr


from math import ceil
from odoo import fields, models, api,_
from openerp.exceptions import ValidationError,UserError
import logging
_logger = logging.getLogger(__name__)



class PurchaseOrderr(models.Model):
    _inherit = "purchase.order"


    @api.depends('payment_term_id','amount_total')
    def _amount_timbre(self):
        for order in self:
            amount_timbre = order.amount_total
            if order.payment_term_id and order.payment_term_id.payment_type == 'cash':
                timbre = self.env['config.timbre']._timbre(order.amount_total)
                self.timbre = timbre['timbre']
                amount_timbre = timbre['amount_timbre']
            self.amount_timbre = amount_timbre
            order.amount_total = self.amount_timbre

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

    payment_type = fields.Char('Type de paiement')
    timbre = fields.Monetary(string='Timbre', store=True, readonly=True,
                             compute='_amount_timbre', track_visibility='onchange')
    amount_timbre = fields.Monetary(string='Total avec Timbre', store=True,
                                    readonly=True, compute='_amount_timbre', track_visibility='onchange')



class SaleOrder(models.Model):
    _inherit = 'sale.order'


    @api.depends('payment_term_id','amount_total')
    def _amount_timbre(self):
        for order in self:
            amount_timbre = order.amount_total
            if order.payment_term_id and order.payment_term_id.payment_type == 'cash':
                timbre = self.env['config.timbre']._timbre(order.amount_total)
                self.timbre = timbre['timbre']
                amount_timbre = timbre['amount_timbre']
            self.amount_timbre = amount_timbre
            order.amount_total = self.amount_timbre

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

    payment_type = fields.Char('Type de paiement')
    timbre = fields.Monetary(string='Timbre', store=True, readonly=True,
                             compute='_amount_timbre', track_visibility='onchange')
    amount_timbre = fields.Monetary(string='Total avec Timbre', store=True,
                                    readonly=True, compute='_amount_timbre')

    # @api.multi
    # def _prepare_invoice(self):
    #     res = super(SaleOrder, self)._prepare_invoice()
    #     res['payment_type'] =  self.payment_type
    #     return res






# ####################################################
# ################### account move ###################
# ####################################################

class AccountMove(models.Model):
    _inherit = "account.move"





    @api.depends(
        'line_ids.matched_debit_ids.debit_move_id.move_id.payment_id.is_matched',
        'line_ids.matched_debit_ids.debit_move_id.move_id.line_ids.amount_residual',
        'line_ids.matched_debit_ids.debit_move_id.move_id.line_ids.amount_residual_currency',
        'line_ids.matched_credit_ids.credit_move_id.move_id.payment_id.is_matched',
        'line_ids.matched_credit_ids.credit_move_id.move_id.line_ids.amount_residual',
        'line_ids.matched_credit_ids.credit_move_id.move_id.line_ids.amount_residual_currency',
        'line_ids.debit',
        'line_ids.credit',
        'line_ids.currency_id',
        'line_ids.amount_currency',
        'line_ids.amount_residual',
        'line_ids.amount_residual_currency',
        'line_ids.payment_id.state',
        'line_ids.full_reconcile_id')
    def _compute_amount(self):
        for move in self:

            if move.payment_state == 'invoicing_legacy':
                # invoicing_legacy state is set via SQL when setting setting field
                # invoicing_switch_threshold (defined in account_accountant).
                # The only way of going out of this state is through this setting,
                # so we don't recompute it here.
                move.payment_state = move.payment_state
                continue

            total_untaxed = 0.0
            total_untaxed_currency = 0.0
            total_tax = 0.0
            total_tax_currency = 0.0
            total_to_pay = 0.0
            total_residual = 0.0
            total_residual_currency = 0.0
            total = 0.0
            total_currency = 0.0
            amount_timbre = 0.0
            currencies = move._get_lines_onchange_currency().currency_id

            for line in move.line_ids:
                if move.is_invoice(include_receipts=True):
                    # === Invoices ===

                    if not line.exclude_from_invoice_tab:
                        # Untaxed amount.
                        total_untaxed += line.balance
                        total_untaxed_currency += line.amount_currency
                        total += line.balance
                        total_currency += line.amount_currency
                        _logger.warning(' \n \n total_currency1***********************total_currency1 %s' %(total_currency))
                    elif line.istimbre:
                        # amount & total amount timbre.
                        amount_timbre += line.amount_currency
                        total_untaxed += line.balance
                        total_untaxed_currency += line.amount_currency
                        total += line.balance
                        total_currency += line.amount_currency
                        _logger.warning(' \n \n total_currency1***********************total_currency1 %s' %(total_currency))
                    elif line.tax_line_id:
                        # Tax amount.
                        total_tax += line.balance
                        total_tax_currency += line.amount_currency
                        total += line.balance
                        total_currency += line.amount_currency
                        _logger.warning(' \n \n total_currency2***********************total_currency2 %s' %(total_currency))
                    elif line.account_id.user_type_id.type in ('receivable', 'payable'):
                        # Residual amount.
                        total_to_pay += line.balance
                        total_residual += line.amount_residual
                        total_residual_currency += line.amount_residual_currency
                else:
                    # === Miscellaneous journal entry ===
                    if line.debit:
                        total += line.balance
                        total_currency += line.amount_currency
                        _logger.warning(' \n \n total_currency3***********************total_currency3 %s' %(total_currency))

            if move.move_type == 'entry' or move.is_outbound():
                sign = 1
            else:
                sign = -1
            move.amount_untaxed = sign * (total_untaxed_currency if len(currencies) == 1 else total_untaxed)
            move.amount_tax = sign * (total_tax_currency if len(currencies) == 1 else total_tax)
            move.amount_total = sign * (total_currency if len(currencies) == 1 else total)
            move.amount_residual = -sign * (total_residual_currency if len(currencies) == 1 else total_residual)
            move.amount_untaxed_signed = -total_untaxed
            move.amount_tax_signed = -total_tax
            move.amount_total_signed = abs(total) if move.move_type == 'entry' else -total
            move.amount_residual_signed = total_residual

            #amount timbre
            move.timbre = abs(amount_timbre) 

            currency = len(currencies) == 1 and currencies or move.company_id.currency_id

            # Compute 'payment_state'.
            new_pmt_state = 'not_paid' if move.move_type != 'entry' else False

            if move.is_invoice(include_receipts=True) and move.state == 'posted':

                if currency.is_zero(move.amount_residual):
                    reconciled_payments = move._get_reconciled_payments()
                    if not reconciled_payments or all(payment.is_matched for payment in reconciled_payments):
                        new_pmt_state = 'paid'
                    else:
                        new_pmt_state = move._get_invoice_in_payment_state()
                elif currency.compare_amounts(total_to_pay, total_residual) != 0:
                    new_pmt_state = 'partial'

            if new_pmt_state == 'paid' and move.move_type in ('in_invoice', 'out_invoice', 'entry'):
                reverse_type = move.move_type == 'in_invoice' and 'in_refund' or move.move_type == 'out_invoice' and 'out_refund' or 'entry'
                reverse_moves = self.env['account.move'].search([('reversed_entry_id', '=', move.id), ('state', '=', 'posted'), ('move_type', '=', reverse_type)])

                # We only set 'reversed' state in cas of 1 to 1 full reconciliation with a reverse entry; otherwise, we use the regular 'paid' state
                reverse_moves_full_recs = reverse_moves.mapped('line_ids.full_reconcile_id')
                if reverse_moves_full_recs.mapped('reconciled_line_ids.move_id').filtered(lambda x: x not in (reverse_moves + reverse_moves_full_recs.mapped('exchange_move_id'))) == move:
                    new_pmt_state = 'reversed'

            move.payment_state = new_pmt_state


    @api.onchange('invoice_payment_term_id')
    def onchange_payment_term_id(self):
        self.payment_type = self.invoice_payment_term_id.payment_type if self.invoice_payment_term_id else False




    payment_type = fields.Char('Type de paiement')
    timbre = fields.Monetary(string='Timbre', store=True, readonly=True, track_visibility='onchange')
    amount_timbre = fields.Monetary(string='Total avec Timbre', store=True, track_visibility='onchange')



    def _recompute_payment_terms_lines(self):
        ''' Compute the dynamic payment term lines of the journal entry.'''
        self.ensure_one()
        self = self.with_company(self.company_id)
        in_draft_mode = self != self._origin
        today = fields.Date.context_today(self)
        self = self.with_company(self.journal_id.company_id)

        def _get_payment_terms_computation_date(self):
            ''' Get the date from invoice that will be used to compute the payment terms.
            :param self:    The current account.move record.
            :return:        A datetime.date object.
            '''
            if self.invoice_payment_term_id:
                return self.invoice_date or today
            else:
                return self.invoice_date_due or self.invoice_date or today

        def _get_timbre_account(self):
            ''' Get the account from timbre configuration pannel.
            :param self:                    The current account.move record.
            :return:                        An account.account record.
            '''

            
            # Search new account.
            domain = [
                ('name', '=', 'Calcul Timbre'),
            ]
            timbre_account = self.env['config.timbre'].search(domain).account_id
            timbre_account_purchase = self.env['config.timbre'].search(domain).account_id_purchase
            if self.move_type in ('in_invoice', 'in_refund'):
                timbre_account = timbre_account_purchase
            if not timbre_account and self.invoice_payment_term_id.payment_type ==  'cash':
                raise ValidationError("Compte De Droit d’enregistrement n'est pas paramétré. \n Allez dans Facturation/Configuration/Configuration Timbre")
            return timbre_account

        def _get_payment_terms_account(self, payment_terms_lines):
            ''' Get the account from invoice that will be set as receivable / payable account.
            :param self:                    The current account.move record.
            :param payment_terms_lines:     The current payment terms lines.
            :return:                        An account.account record.
            '''
            if payment_terms_lines:
                if self.invoice_payment_term_id.name == 'Espèce (Timbre)':
                    return _get_timbre_account(self)
                # Retrieve account from previous payment terms lines in order to allow the user to set a custom one.
                else:
                    return payment_terms_lines[0].account_id
            elif self.partner_id:
                # Retrieve account from partner.
                if self.is_sale_document(include_receipts=True):
                    return self.partner_id.property_account_receivable_id
                else:
                    return self.partner_id.property_account_payable_id
            else:
                # Search new account.
                domain = [
                    ('company_id', '=', self.company_id.id),
                    ('internal_type', '=', 'receivable' if self.move_type in ('out_invoice', 'out_refund', 'out_receipt') else 'payable'),
                ]
                return self.env['account.account'].search(domain, limit=1)



        def _compute_timbre(self,total_balance ):
            today_date = fields.Date.context_today(self)
            result = []
            _logger.warning(' \n total_balance*********************** total_balance %s' %(total_balance))
            amount_timbre = abs(total_balance)
            if self.invoice_payment_term_id and self.invoice_payment_term_id.payment_type == 'cash':
                timbre = self.env['config.timbre']._timbre(amount_timbre)
                amount_timbre = timbre['timbre'] if self.move_type in ('out_invoice') else -timbre['timbre']
                amount_timbre_total = timbre['amount_timbre'] if self.move_type in ('in_invoice') else - timbre['amount_timbre']
            result.append((today_date, amount_timbre_total, amount_timbre))
            _logger.warning('  result*********************** result %s' %(result))
            return result



        def _compute_payment_terms(self, date, total_balance, total_amount_currency):
            ''' Compute the payment terms.
            :param self:                    The current account.move record.
            :param date:                    The date computed by '_get_payment_terms_computation_date'.
            :param total_balance:           The invoice's total in company's currency.
            :param total_amount_currency:   The invoice's total in invoice's currency.
            :return:                        A list <to_pay_company_currency, to_pay_invoice_currency, due_date>.
            '''
            if self.invoice_payment_term_id:
                to_compute = self.invoice_payment_term_id.compute(total_balance, date_ref=date, currency=self.company_id.currency_id)
                if self.currency_id == self.company_id.currency_id:
                    # Single-currency.
                    return [(b[0], b[1], b[1]) for b in to_compute]
                else:
                    # Multi-currencies.
                    to_compute_currency = self.invoice_payment_term_id.compute(total_amount_currency, date_ref=date, currency=self.currency_id)
                    return [(b[0], b[1], ac[1]) for b, ac in zip(to_compute, to_compute_currency)]
            else:
                return [(fields.Date.to_string(date), total_balance, total_amount_currency)]


        def _compute_diff_payment_terms_lines(self, existing_terms_lines, account, to_compute, to_timbre):
            ''' Process the result of the '_compute_payment_terms' method and creates/updates corresponding invoice lines.
            :param self:                    The current account.move record.
            :param existing_terms_lines:    The current payment terms lines.
            :param account:                 The account.account record returned by '_get_payment_terms_account'.
            :param to_compute:              The list returned by '_compute_payment_terms'.
            '''
            # As we try to update existing lines, sort them by due date.
            existing_terms_lines = existing_terms_lines.sorted(lambda line: line.date_maturity or today)
            existing_terms_lines_index = 0

            # Recompute amls: update existing line or create new one for each payment term.
            new_terms_lines = self.env['account.move.line']
            i = 0
            _logger.warning(' \n to_compute*********************** to_compute %s' %(to_compute))
            for date_maturity, balance, amount_currency in to_compute:
                currency = self.journal_id.company_id.currency_id
                if currency and currency.is_zero(balance) and len(to_compute) > 1:
                    continue

                if self.invoice_payment_term_id.name != 'Espèce (Timbre)':
                    if existing_terms_lines_index < len(existing_terms_lines):
                        # Update existing line.
                        candidate = existing_terms_lines[existing_terms_lines_index]
                        existing_terms_lines_index += 1
                        _logger.warning(' \n \n balance***********************balance foi %s' %(balance))
                        candidate.update({
                            'date_maturity': date_maturity,
                            'amount_currency': -amount_currency,
                            'debit': balance < 0.0 and -balance or 0.0,
                            'credit': balance > 0.0 and balance or 0.0,
                        })
                    else:
                        # Create new line.
                        create_method = in_draft_mode and self.env['account.move.line'].new or self.env['account.move.line'].create
                        candidate = create_method({
                            'name': self.payment_reference or '',
                            'debit': balance < 0.0 and -balance or 0.0,
                            'credit': balance > 0.0 and balance or 0.0,
                            'quantity': 1.0,
                            'amount_currency': -amount_currency,
                            'date_maturity': date_maturity,
                            'move_id': self.id,
                            'currency_id': self.currency_id.id,
                            'account_id': account.id,
                            'partner_id': self.commercial_partner_id.id,
                            'exclude_from_invoice_tab': True,
                        })
                    new_terms_lines += candidate

                    if in_draft_mode:
                        candidate.update(candidate._get_fields_onchange_balance(force_computation=True))
                else:
                    for date_maturity, amount_timbre_total, amount_timbre in to_timbre:
                        for i in range(2):
                            
                            if i == 0:
                                candidate = existing_terms_lines[0]
                                # existing_terms_lines_index += 1
                                candidate.update({
                                        'name': '',
                                        'date_maturity': date_maturity,
                                        'amount_currency': -amount_timbre_total,
                                        'debit': amount_timbre_total < 0.0 and -amount_timbre_total or 0.0,
                                        'credit': amount_timbre_total > 0.0 and amount_timbre_total or 0.0,
                                    })
                            else:
                                create_method = in_draft_mode and self.env['account.move.line'].new or self.env['account.move.line'].create
                                _logger.warning(' \n \n amount_timbre***********************amount_timbre %s' %(amount_timbre))
                                candidate2 = create_method({
                                    'name': 'Timbre' ,
                                    'debit': amount_timbre < 0.0 and -amount_timbre or 0.0,
                                    'credit': amount_timbre > 0.0 and amount_timbre or 0.0,
                                    'quantity': 1.0,
                                    'amount_currency': -amount_timbre,
                                    'move_id': self.id,
                                    'currency_id': self.currency_id.id,
                                    'account_id': account.id,
                                    'partner_id': self.commercial_partner_id.id,
                                    'exclude_from_invoice_tab': True,
                                    'istimbre' : True,
                                })
                            # candidate += candidate 
                        new_terms_lines +=  candidate2 + candidate
                        if in_draft_mode:
                            candidate2.update(candidate2._get_fields_onchange_balance(force_computation=True))
                            candidate.update(candidate._get_fields_onchange_balance(force_computation=True))

                # if in_draft_mode:
                #     candidate.update(candidate._get_fields_onchange_balance(force_computation=True))
            return new_terms_lines



        existing_terms_lines = self.line_ids.filtered(lambda line: line.account_id.user_type_id.type in ('receivable', 'payable') )
        others_lines = self.line_ids.filtered(lambda line: line.account_id.user_type_id.type not in ('receivable', 'payable') )
        timbre_account_id = _get_timbre_account(self)
        timbre_lines = self.line_ids.filtered(lambda line: line.account_id.code in (timbre_account_id.code))
        company_currency_id = (self.company_id or self.env.company).currency_id
        total_balance = sum(others_lines.filtered(lambda line: line.account_id.code not in (timbre_account_id.code)).mapped(lambda l: company_currency_id.round(l.balance)))
        total_amount_currency = sum(others_lines.mapped('amount_currency'))

        # timbre_lines = self.line_ids.filtered(lambda line: line.account_id.user_type_id in ('Current Liabilities') )


        if not others_lines:
            self.line_ids -= existing_terms_lines
            return

        computation_date = _get_payment_terms_computation_date(self)
        account = _get_payment_terms_account(self, existing_terms_lines)
        to_compute = _compute_payment_terms(self, computation_date, total_balance, total_amount_currency)
        to_timbre  = _compute_timbre(self, total_balance) if self.invoice_payment_term_id.name  == 'Espèce (Timbre)' else 0
        new_terms_lines = _compute_diff_payment_terms_lines(self, existing_terms_lines, account, to_compute, to_timbre)




        # Remove old terms lines that are no longer needed.
        self.line_ids -= existing_terms_lines - new_terms_lines 
        self.line_ids -=  timbre_lines

        if new_terms_lines:
            self.payment_reference = new_terms_lines[-1].name or ''
            self.invoice_date_due = new_terms_lines[-1].date_maturity




class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    _order = "date desc, move_name desc, id"


    @api.depends('name')
    def _get_compute_istimbre(self):
        for rec in self:
            if rec.name == 'Timbre':
                rec.istimbre = True
            else:
                rec.istimbre = False


    istimbre = fields.Boolean(compute="_get_compute_istimbre", store=True)


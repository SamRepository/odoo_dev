# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
#
# Copyright (c) 2016  - Osis - www.osis-dz.net


import logging
import locale
import decimal

import odoo
from odoo import api, fields, models, tools, _
from odoo.tools.safe_eval import safe_eval
from odoo.exceptions import UserError, ValidationError
from odoo.addons import decimal_precision as dp

_logger = logging.getLogger(__name__)


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    @api.multi
    def compute_sheet(self):	
 	payslip_line_obj = self.env['hr.payslip.line']
        for payslip in self:
            number = payslip.number or self.env['ir.sequence'].next_by_code('salary.slip')
            #delete old payslip lines
	    line = payslip_line_obj.search([('slip_id','=', payslip.id)])
            line.unlink()
            # set the list of contract for which the rules have to be applied
            # if we don't give the contract, then the rules to apply should be for all current contracts of the employee
            contract_ids = payslip.contract_id.ids or \
                self.get_contract(payslip.employee_id, payslip.date_from, payslip.date_to)
            lines = [(0, 0, line) for line in self.get_payslip_lines(contract_ids, payslip.id)]
            payslip.write({'line_ids': lines, 'number': number})
        return True

    @api.model
    def get_worked_day_lines(self, contract_ids, date_from, date_to):
        res = super(HrPayslip, self).get_worked_day_lines(contract_ids, date_from, date_to)
	user = self._context.get('uid')
	company_id = self.env.user.company_id
        number_of_days =  company_id.days
        number_of_hours = company_id.hours
        for line in res:
            if 'number_of_days' in line:
                line['number_of_days'] =number_of_days
                line['number_of_hours']=number_of_hours
        return res

    @api.one
    @api.depends('line_ids.total')
    def _compute_net(self):
        self.net = sum(line.total for line in self.line_ids if line.code<>'R999' )

    net = fields.Float(string='Net à payer',
        store=True, readonly=True, compute='_compute_net', digits=dp.get_precision('Payroll'))


class HrPayslipLine(models.Model):
    _inherit = 'hr.payslip.line'

    @api.depends('quantity', 'amount', 'rate')
    def _compute_total(self):
        for line in self:
            total = float(line.quantity) * line.amount * line.rate / 100
            line.total = decimal.Decimal(total).quantize(decimal.Decimal('.1'), rounding=decimal.ROUND_UP)

class HrSalaryRule(models.Model):
    _inherit = 'hr.salary.rule'
    _order = 'sequence, code, id'

    @api.model
    def _callback(self, model_name, method_name, qty):
        if self.pool != self.pool.check_signaling():
            self.env.reset()
            self = self.env()[self._name]
        if model_name in self.env:
            model = self.env[model_name]
            if hasattr(model, method_name):
               res = getattr(model, method_name)(qty)
            else:
              _logger.warning("Method '%s.%s' does not exist.", model_name, method_name)
        else:
           _logger.warning("Model %r does not exist.", model_name)
        return res

    model = fields.Char(string='Object', help="Model name on which the method to be called is located, e.g. 'res.partner'.")
    function = fields.Char(string='Method', help="Name of the method to be called when this job is processed.")
    amount_select = fields.Selection([
        ('percentage', 'Percentage (%)'),
        ('fix', 'Fixed Amount'),
        ('code', 'Python Code'),
        ('function', 'Function')
    ], string='Amount Type', index=True, required=True, default='fix', help="The computation method for the rule amount.")
  
  
    #TODO should add some checks on the type of result (should be float)
    @api.multi
    def compute_rule(self, localdict):

        self.ensure_one()
        if self.amount_select == 'fix':
            try:
                return self.amount_fix, float(safe_eval(self.quantity, localdict)), 100.0
            except:
                raise UserError(_('Wrong quantity defined for salary rule %s (%s).') % (self.name, self.code))
        elif self.amount_select == 'percentage':
            try:
                return (float(safe_eval(self.amount_percentage_base, localdict)),
                        float(safe_eval(self.quantity, localdict)),
                        self.amount_percentage)
            except:
                raise UserError(_('Wrong percentage base or quantity defined for salary rule %s (%s).') % (self.name, self.code))
        elif self.amount_select == 'function':
            try:
                qty = float(safe_eval(self.quantity, localdict))
                callback = self._callback(self.model, self.function, qty)
                return callback, 1.0, 100.0
            except:
                raise UserError(_('Wrong function defined for salary rule %s (%s).') % (self.name, self.code))
        else:
            try:
                safe_eval(self.amount_python_compute, localdict, mode='exec', nocopy=True)
                return float(localdict['result']), 'result_qty' in localdict and localdict['result_qty'] or 1.0, 'result_rate' in localdict and localdict['result_rate'] or 100.0
            except:
                raise UserError(_('Wrong python code defined for salary rule %s (%s).') % (self.name, self.code))
   

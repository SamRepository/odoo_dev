# -*- coding: utf-8 -*-

from odoo import tools
from odoo import models, fields, api


class HrPaslipReport(models.Model):
    _name = "hr.payslip.report"
    _description = "payslip Statistics"
    _auto = False

    date = fields.Date(readonly=True)
    employee_id = fields.Many2one('hr.employee', string='Employe', readonly=True)
    company_id = fields.Many2one('res.company', string='Company', readonly=True)
    salary_rule_id = fields.Many2one('hr.salary.rule', string='Rule', readonly=True)
    quantity = fields.Float(string='Base', readonly=True)
    amount = fields.Float(string='Amount', readonly=True)
    total = fields.Float(string='Total', readonly=True)
    category_id = fields.Many2one('hr.salary.rule.category', string='Category', readonly=True)
    nbr = fields.Integer(string='# of Lines', readonly=True)  # TDE FIXME master: rename into nbr_lines
    state = fields.Selection([
        ('draft', 'Draft'),
        ('verify', 'Waiting'),
        ('done', 'Done'),
        ('cancel', 'Rejected')
        ], string='Payslip Status', readonly=True)

    _order = 'date desc'

    def _select(self):
        select_str = """
        SELECT
        min(l.id) as id,
                    l.salary_rule_id as salary_rule_id,
		    l.category_id as category_id,
                    i.date_from as date,
                    i.state,
                    i.employee_id as employee_id,
                    i.company_id as company_id,
                    SUM(l.quantity) as quantity,
                    SUM(l.amount) as amount,
                    SUM(l.total) as total
      FROM hr_payslip i
         LEFT JOIN hr_payslip_line l on (l.slip_id=i.id) 
		WHERE l.appears_on_payslip = True AND l.code <> 'R999'
                GROUP BY l.salary_rule_id, i.date_from, i.employee_id, i.state, i.company_id, l.category_id
        """
        return select_str

    @api.model_cr
    def init(self):
        # self._table = sale_report
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (
            %s
            )""" % (self._table, self._select()))


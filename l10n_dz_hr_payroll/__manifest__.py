# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
#
# Copyright (c) 2016  - Osis - www.osis-dz.net

{
    'name': 'Algeria - Payroll',
    'version': '0.3',
    'category': 'Localization',
    'description': """
This is the module to manage Algeria payslip in Odoo.
========================================================================

	- This module applies to companies based in Algeria.
    	- All main contributions rules for Algeria payslip.
    	- New payslip report.
	- New statistic report.
TODO:
-----

http://www.slideshare.net/yacinebensidhoum/paie-algrienne-odoo
**Email:** contact@osis.dz
""",
    'author': 'Osis',
    'website': 'http://www.osis-dz.net/',
    'depends': ['hr_payroll', 'l10n_dz', 'smile_decimal_precision'],
    'data': [

        'security/ir.model.access.csv',
        'data/l10n_dz_hr_payroll_data.xml',
    	'views/l10n_dz_hr_payroll_config_settings_views.xml',
    	'views/hr_empolyee_view.xml',
    	'views/hr_payroll_view.xml',
        'report/report_l10ndzfichepaye.xml',
        'report/l10n_dz_hr_payroll_report.xml',
	'reports/hr_payslip_report_view.xml',
        'views/l10n_dz_hr_payroll_config_settings_views.xml',
    ],

    'demo': ['demo/l10n_dz_hr_payroll_demo.xml'],

    'installable': True,
    'application': False,
    'auto_install': False,
}

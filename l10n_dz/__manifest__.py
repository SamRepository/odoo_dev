# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
#
# Copyright (c) 2016  - Osis - www.osis-dz.net

{
    'name': 'Algeria - Accounting',
    'version': '1.1',
    'category': 'Localization',
    'description': """
This is the module to manage the accounting chart for Algeria in Odoo.
========================================================================

This module applies to companies based in Algeria.
.

**Email:** contact@osis.dz
""",
    'author': 'Osis',
    'website': 'http://www.osis-dz.net/',
    'depends': ['account','l10n_dz_region'],
    'data': [
        'data/wizard_data.xml',
        'data/plan_comptable_data.xml',
        'views/l10n_dz_view.xml',
        'data/account_tax_data.xml',
        'data/account_fiscal_position_template_data.xml',
        'data/account_chart_template_data.yml',
    ],

    'installable': True,
    'application': False,
    'auto_install': False,
}

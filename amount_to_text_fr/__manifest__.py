# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
#
# Copyright (c) 2016  - Osis - www.osis-dz.net

{
    'name': 'Amount to Text',
    'version': '0.3',
    'category': 'Accounting',
    'description': """
This is the module print amount to Text .
========================================================================


**Email:** contact@osis.dz
""",
    'author': 'Osis',
    'website': 'http://www.osis-dz.net/',
    'depends': ['account','sale'],
    'data': [
        'views/order_invoice.xml',
        'views/header_footer.xml',

    ],

    'installable': True,
    'application': False,
    'auto_install': False,
}

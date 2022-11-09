# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
#
# Copyright (c) 2022  - samir.sellami@live.fr

{
    'name': 'Algérie - Timbre Fiscal',
    'summary': "Module Odoo pour ajouter le Timbre Fiscal avec ecritures comptables",
    'description': """ Le module vous permet de choisir le mode de paiement Esp&#232;ce Timbre dont le timbre comme &#233;criture comptable et inclus dans le TTC
    ========================================================================
    This module applies to companies based in Algeria.
    .
    **Email:** samir.sellami@live.fr
    """,
    'author': 'samir.sellami@live.fr, ENSET-Skikda',
    'website': 'https://sites.google.com/view/samir-sellami',
    'version': '14.0.2.1',
    'category': 'Accounting',
    # any module necessary for this one to work correctly
    'depends': ['sale','account','purchase', 'base'],
    'application': True,
    'sequence': 5,
    'installable': True,
    'auto_install': False,
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/timbre_data.xml',
        'data/res.bank.csv',
        'views/timbre_view.xml',
        'views/sale_invoice_view.xml',
    ],
    'images': ['static/description/banner.jpg'],
}

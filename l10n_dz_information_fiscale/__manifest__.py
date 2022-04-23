# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
#
# Copyright (c) 2022  - samir.sellami@live.fr

{
    'name': "Algérie - Information Fiscale",
    'summary': """ Information Fiscale pour les entreprises en Algérie """,
    'description': """
This is the module to manage fiscal information for Algeria companies in Odoo.
========================================================================
This module applies to companies based in Algeria.
.
**Email:** samir.sellami@live.fr
""",
    'author': 'samir.sellami@live.fr, ENSET-Skikda',
    'website': 'https://sites.google.com/view/samir-sellami',
    'version': '14.0.2.0',
    'category': 'Accounting',
    # any module necessary for this one to work correctly
    'depends': ['base','account',],
    'application': ['True'],
    'sequence': 3,
    'installable': True,
    'auto_install': False,
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/forme_juridique_datas.xml',
        'views/forme_juridique.xml',
        'views/res_company.xml',
        'views/res_partner.xml',
    ],
}
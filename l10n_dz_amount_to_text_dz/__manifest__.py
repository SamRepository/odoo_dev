# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
#
# Copyright (c) 2022  - samir.sellami@live.fr
{
    'name': "Algérie - Montant en lettres DZ",
    'summary': """ Montant en lettres DZ - odoo 14 """,
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
    'category': 'Outils',
    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'sale',],
    'application': ['True'],
    'sequence': 4,
    'installable': True,
    'auto_install': False,
    # always loaded
    'data': [],
}
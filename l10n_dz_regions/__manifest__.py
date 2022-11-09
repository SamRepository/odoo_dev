# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
#
# Copyright (c) 2022  - samir.sellami@live.fr

{
    'name': "Algérie - Wilayas et Communes",
    'summary': "Module Odoo pour ajouter les 58 Wilayas et leurs Communes de Algérie",
    'description': """
This is the module to manage the wilaya & commune for Algeria in Odoo.
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
    'depends': ['sale'],
    'application': True,
    'sequence': 2,
    'installable': True,
    'auto_install': False,
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/wilayas_data.xml',
        'data/commune_data.xml',
        'views/res_commune.xml'
    ],
    'images': ['static/description/banner.jpg'],
}


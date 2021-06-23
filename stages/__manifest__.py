# -*- coding: utf-8 -*-
{
    'name': "Gestion des Stages",
    'summary': "Module Odoo pour gérer les stages de perfectionnement au niveau de l'ENSET-Skikda",
    'description': """
        Long description of module's purpose
    """,
    'author': "ENSET-Skikda",
    'website': "www.enset-skikda.dz",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Education',
    'version': '12.0.0.2',
    # any module necessary for this one to work correctly
    'depends': ['base','contacts','hr','event','account',],
    'application': ['True'],
    'sequence': 1,
    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
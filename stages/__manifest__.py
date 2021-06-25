# -*- coding: utf-8 -*-
{
    'name': "Gestion des Stages",
    'summary': "Module Odoo pour gérer les stages de perfectionnement au niveau de l'ENSET-Skikda",
    'description': """
        Long description of module's purpose """,
    'author': "ENSET-Skikda",
    'website': "www.enset-skikda.dz",
    'category': 'Education',
    'version': '12.0.0.2',
    # any module necessary for this one to work correctly
    'depends': ['base','contacts','hr','event','account',],
    'application': ['True'],
    'sequence': 1,
    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views_main.xml',
        'views/templates.xml',
        'views/stages_candidature_views.xml',
        'views/stages_enseignant_views.xml',
        'views/stages_departement_views.xml',
        'views/stages_organisme_views.xml',
        'views/stages_session_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
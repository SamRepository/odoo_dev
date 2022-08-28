# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
#
# Copyright (c) 2022  - samir.sellami@live.fr

{
    'name': "Gestion des Stages",
    'summary': "Module Odoo pour gérer les stages de perfectionnement au niveau de l'ENSET-Skikda",
    'description': """
        Long description of module's purpose """,
    'author': "ENSET-Skikda",
    'website': "www.enset-skikda.dz",
    'category': 'Stages Category',
    'version': '14.0.0.2',
    # any module necessary for this one to work correctly
    'depends': ['base','l10n_dz_regions','contacts','hr','event','account','mail','website'],
    'application': ['True'],
    'sequence': 1,
    # always loaded
    'data': [
        'security/stages_security.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'reports/report_departement_list.xml',
        'reports/departement_list_report.xml',
        'wizard/stages_candidature_chg_period_view.xml',
        'views/views_main.xml',
        'views/templates.xml',
        'views/website_menus.xml',
        'views/stages_portal_templates.xml',
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
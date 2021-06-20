# -*- coding: utf-8 -*-

from odoo import models, fields, api,  _

class StagesExercice(models.Model):
    _name = 'stages.exercice'
    _description = 'Exercice Fiscal - السنة المالية'
    _rec_name = 'annee'

    annee = fields.Date(string="Année Fiscal - السنة المالية", required=True, )
    texte_reglmtr = fields.Text(string="Textes Réglementaires - النصوص التنظيمية", )
    chapitre = fields.Char(string="Chapitre - الفصل", required=False)
    articles = fields.Char(string="Articles - الحسابات", required=False)
    budget_max = fields.Float(string="Budget Exercice - الميزانية",  required=True, )
    budget_suppl = fields.Float(string="Budget Suplimentaire - الميزانية الاضافية", required=True, )
# -*- coding: utf-8 -*-

from odoo import models, fields, api,  _

class StagesExercice(models.Model):
    _name = 'stages.exercice'
    _description = 'Exercice Fiscal'
    _rec_name = 'annee'

    annee = fields.Date(string="Année Fiscal", required=True, )
    texte_reglmtr = fields.Text(string="Textes Réglementaires", )
    chapitre = fields.Char(string="Chapitre", required=False)
    articles = fields.Char(string="Articles", required=False)
    budget_max = fields.Float(string="Budget Exercice",  required=True, )
    budget_suppl = fields.Float(string="Budget Suplimentaire", required=True, )
# -*- coding: utf-8 -*-

from odoo import models, fields, api,  _

class StagesTypeStage(models.Model):
    _name = 'stages.type_stage'
    _description = 'Catégories Stages - انواع التربصات'
    _rec_name = 'name'

    name = fields.Char(string="Intitulé stage - إسم التربص", required=True)
    conditions = fields.Text("Conditions stage - شروط التربص ", required=False,)
#   indemnite_stage_ids = fields.One2many(comodel_name="", inverse_name="", string="", required=False, )
#    grades_ids = fields.One2many(comodel_name="stages.type_stage.grades", inverse_name="type_stage_id", string="Grades Concernés - الرتب العلمية المعنية", )
    grades_ids = fields.Many2many(comodel_name="stages.grade", relation="", column1="", column2="", string="Grades Concernés - الرتب العلمية المعنية", )
    indemnite_stage_ids = fields.One2many(comodel_name="stages.type_stage.indemnite", inverse_name="type_stage_id",
                                 string="Indemnite Stage par zone- علاوات لتربص حسب المنطقة", )

# class StagesStageTypeGrades(models.Model):
#     _name = 'stages.type_stage.grades'
#     _description = 'Grades Concernés par Stage - الرتب العلمية المعنية بالتربص'
#
#     grade_id= fields.Many2one(comodel_name="stages.grade", string= "Grades Scientifiques - الرتب العلمية",)
#     type_stage_id = fields.Many2one(comodel_name="stages.type_stage", string="Type Stage - نوع التربص",)

class StagesStageTypeIndemnite(models.Model):
    _name = 'stages.type_stage.indemnite'
    _description = 'Indemnite Stage par zone - علاوات التربص حسب المنطقة'
    _rec_name = 'zone_id'

    nombre_jour = fields.Integer(string="Nombre de jour - عدد الايام", required=False, )
    montant= fields.Float(string="Montant - القيمة",  required=False, )
    montant_lettre_fr = fields.Char(string="Montant lettre fr - بالفرنسية", required=False, )
    montant_lettre_ar = fields.Char(string="Montant lettre ar - بالعربية", required=False, )
    zone_id= fields.Many2one(comodel_name="res.country.group", string= "Zone - المناطق",)
    type_stage_id = fields.Many2one(comodel_name="stages.type_stage", string="Type Stage - نوع التربص",)
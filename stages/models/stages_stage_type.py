# -*- coding: utf-8 -*-

from odoo import models, fields, api,  _

class StagesStageType(models.Model):
    _name = 'stages.stage_type'
    _description = 'Catégories Stages'
    _rec_name = 'name'

    name = fields.Char(string="Intitulé", required=True)
    conditions = new_field = fields.Text(string="Conditions Stage", required=False, )
    stage_type_grades = fields.One2many(comodel_name="stages.stage_type.grades", inverse_name="stage_type_id", string="Grades du Stage", )

class StagesStageTypeGrades(models.Model):
    _name = 'stages.stage_type.grades'
    _description = 'Grades Autorisés par Stage '

    grade_id= fields.Many2one(comodel_name="stages.grade", string="Grade", )
    stage_type_id = fields.Many2one(comodel_name="stages.stage_type", string="Stage Type ID",)
# -*- coding: utf-8 -*-

from odoo import models, fields, api,  _

class StagesStageType(models.Model):
    _name = 'stages.stage_type'
    _description = 'Catégories Stages - انواع التربصات'
    _rec_name = 'name'

    name = fields.Char(string="Intitulé stage - إسم التربص", required=True)
    conditions = fields.Text(string="Conditions stage - شروط التربص ", required=False, )
    stage_type_grades = fields.One2many(comodel_name="stages.stage_type.grades", inverse_name="stage_type_id", string="Grades Concernés - الرتب العلمية المعنية", )

class StagesStageTypeGrades(models.Model):
    _name = 'stages.stage_type.grades'
    _description = 'Grades Concernés par Stage - الرتب العلمية المعنية بالتربص'

    grade_id= fields.Many2one(comodel_name="stages.grade", string= "Grades Scientifiques - الرتب العلمية",)
    stage_type_id = fields.Many2one(comodel_name="stages.stage_type", string="Type Stage - نوع التربص",)
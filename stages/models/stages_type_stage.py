# -*- coding: utf-8 -*-

from odoo import models, fields, api,  _

class StagesTypeStage(models.Model):
    _name = 'stages.type_stage'
    _description = 'Catégories Stages - انواع التربصات'
    _rec_name = 'name'

    name = fields.Char(string="Intitulé stage - إسم التربص", required=True)
    conditions = fields.Text(string="Conditions stage - شروط التربص ", required=False, )
    indemnite_stage = fields.Float(string="Indémnite Stage - علاوة التربص",  required=False, )
    grades_ids = fields.One2many(comodel_name="stages.type_stage.grades", inverse_name="type_stage_id", string="Grades Concernés - الرتب العلمية المعنية", )

class StagesStageTypeGrades(models.Model):
    _name = 'stages.type_stage.grades'
    _description = 'Grades Concernés par Stage - الرتب العلمية المعنية بالتربص'

    grade_id= fields.Many2one(comodel_name="stages.grade", string= "Grades Scientifiques - الرتب العلمية",)
    type_stage_id = fields.Many2one(comodel_name="stages.type_stage", string="Type Stage - نوع التربص",)
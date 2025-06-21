from random import randint

from odoo import fields, models


class TopicCategory(models.Model):

    _name = "pfe.topic_category"
    _description = "Topic Category"

    def _get_default_color(self):
        return randint(1, 11)

    name = fields.Char(string="Tag Name", required=False)
    color = fields.Integer(string='Color Index', default=_get_default_color)
    topic_ids = fields.Many2many('pfe.topic', 'topic_category_rel', 'category_id', 'emp_id', string='Topic')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists !"),
    ]
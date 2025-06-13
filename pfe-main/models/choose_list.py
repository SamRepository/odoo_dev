from odoo import models, fields,api

class Choose(models.Model):
    _name = 'pfe.choose_list'
    _description = 'List of dissertation choices by group'
    group_id = fields.Many2one('pfe.sgroupe', string="Student's Group", required=True, ondelete='cascade')
    dissertation_id = fields.Many2one('pfe.dissertation', string="Dissertation", required=True)
    sequence = fields.Integer( compute='set_seq',string='sequence')
    _sql_constraints = [
        ('group_dissertation_sequence_unique',
         'UNIQUE(group_id, sequence)',
         'Each group must have a unique sequence for each dissertation choice.')
    ]
    @api.depends('dissertation_id')
    def set_seq(self):
        for record in self:
            if record.group_id:
                group_choices = self.filtered(lambda r: r.group_id == record.group_id)
                sorted_choices = sorted(group_choices, key=lambda r: r.id or 0)
                for index, rec in enumerate(sorted_choices, start=1):
                    rec.sequence = index
            else:
                record.sequence = 0  # default fallback


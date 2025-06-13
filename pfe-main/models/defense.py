from odoo import models, fields, api
from odoo.exceptions import ValidationError
class Defense(models.Model):
    _name = 'pfe.defense'
    _description = 'Soutenance de PFE'
    group_id = fields.Many2one('pfe.sgroupe', string="Student's Group", required=True)
    dissertation_id = fields.Many2one('pfe.dissertation', string="Dissertation", required=True)
    jury_ids = fields.Many2many('hr.employee', string="Jury Members")
    date = fields.Date(string="Defense Date")
    time = fields.Float(string="Time")
    location = fields.Char(string="Classroom")
    final_grade = fields.Float(string="Final Grade")
    dissertation_file = fields.Binary(string="Dissertation File")
    dissertation_filename = fields.Char(string="File Name")
    comments = fields.Text(string="Juries Comments")
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('planned', 'Planifiée'),
        ('done', 'Validée')
    ], string="État", default='draft')

    @api.model
    def create(self, vals):
        record = super().create(vals)
        record._assign_jury_tags()
        return record

    def write(self, vals):
        res = super().write(vals)
        self._assign_jury_tags()
        return res

    def _assign_jury_tags(self):
        jury_tag = self.env.ref('pfe.tag_jury', raise_if_not_found=False)
        if jury_tag:
            for rec in self:
                for member in rec.jury_ids:
                    if jury_tag not in member.category_ids:
                        member.category_ids |= jury_tag

    def action_valider_soutenance(self):
        for rec in self:
            if not rec.final_grade:
                raise ValidationError("Veuillez entrer la note finale avant de valider la soutenance.")
            rec.state = 'done'

    def action_generate_pv(self):
        return self.env.ref('pfe.action_report_defense_pv').report_action(self)

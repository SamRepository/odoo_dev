from odoo import models, fields, api, exceptions, _
from odoo.exceptions import UserError
from datetime import date


class Topic(models.Model):
    _name = 'pfe.topic'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _description = 'Dissertation Topic'
    _rec_name = 'name'
    name = fields.Char(
        string="SEQ",
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: self.env['ir.sequence'].next_by_code('pfe.topic')
    )
    title= fields.Char(string="Topic Title", required=True)

    description = fields.Html(string="Description")
    tools = fields.Html(string="Tools")
    reference = fields.Char(string="Reference", required=True)
    attachment_ids = fields.Many2many(
        'ir.attachment',
        string="Attachments",
        help="You can attach files like PDF, images, etc."
    )
    state = fields.Selection([
        ('pending', 'Pending'),
        ('validated', 'Validated'),
        ('rejected', 'Rejected'),
    ], string="State", default='pending', tracking=True)
    category_ids = fields.Many2many(
        'pfe.topic_category', 'topic_category_rel',
        'emp_id', 'category_id',
        string='Tags')
    supervisor_id = fields.Many2one('hr.employee', string="Supervisor", tracking=True)
    dissertation_id = fields.Many2one('pfe.dissertation', string="Dissertation", readonly=True)

    _sql_constraints = [
        ('unique_topic_name', 'UNIQUE(name)', 'Topic title must be unique!'),
    ]

    @api.model
    def create(self, vals):
        # توليد الرقم التسلسلي
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('pfe.topic') or _('New')

        # إضافة فئة Teacher إذا لم تكن موجودة
        if 'supervisor_id' in vals:
            supervisor = self.env['hr.employee'].browse(vals['supervisor_id'])
            category_teacher = self.env.ref('pfe.category_teacher')
            if category_teacher not in supervisor.category_ids:
                supervisor.category_ids = [(4, category_teacher.id)]

        return super(Topic, self).create(vals)

    def action_validate_button(self):
        if not self.env.user.sudo().has_group('pfe.group_committee_scientifique'):
            raise UserError("Seul le Comité Scientifique peut valider un sujet.")

        self.state = 'validated'

        if not self.dissertation_id:
            dissertation = self.create_dissertation()

        supervisor = self.supervisor_id.sudo()
        if supervisor:
            supervisor_category = self.env.ref('pfe.category_supervisor').sudo()
            if supervisor_category not in supervisor.category_ids:
                supervisor.category_ids = [(4, supervisor_category.id)]

        # عرض أطروحة مباشرة بعد الإنشاء
        context = dict(self.env.context)
        context['form_view_initiale_mode'] = 'edit'
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'pfe.dissertation',
            'res_id': self.dissertation_id.id,
            'context': context,
        }

    def action_set_pending_button(self):
        if not self.env.user.sudo().has_group('pfe.group_committee_scientifique'):
            raise UserError("Seul le Comité Scientifique peut changer l'état du sujet.")
        self.state = 'pending'

    def action_reset_to_proposed(self):
        raise UserError("The proposed state has been removed.")

    def action_reject_button(self):
        if not self.env.user.sudo().has_group('pfe.group_committee_scientifique'):
            raise UserError("Seul le Comité Scientifique peut rejeter un sujet.")
        self.state = 'rejected'

    def create_dissertation(self):
        if self.state != 'validated':
            raise UserError("Only validated Topics can have a Dissertation.")
        if not self.id:
            raise UserError("The Topic must be saved before creating a Dissertation.")

        dissertation_vals = {
            'title': self.title,
            'description': self.description,
            'tools': self.tools,
            'reference': self.reference,
            'topic_id': self.id,
            'supervisor_id': self.supervisor_id.id if self.supervisor_id else False,
            'attachment_ids': [(6, 0, self.attachment_ids.ids)],
            'category_ids': [(6, 0, self.category_ids.ids)],

        }
        dissertation = self.env['pfe.dissertation'].create(dissertation_vals)
        self.dissertation_id = dissertation.id
        return dissertation

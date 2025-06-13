from odoo import models, fields,exceptions

class Dissertation(models.Model):
    _name = 'pfe.dissertation'
    _description = 'Dissertation'
    _rec_name="name"
    name = fields.Char(
        string="SEQ",
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: self.env['ir.sequence'].next_by_code('pfe.topic')
    )
    title = fields.Char(string="Title", required=False)
    description = fields.Html(string="Description")
    tools = fields.Html(string="Tools")
    reference = fields.Char(string="Reference")
    attachment_ids = fields.Many2many(
        'ir.attachment',
        string="Attachments",
        help="You can attach files like PDF, images, etc."
    )
    category_ids = fields.Many2many(
        'pfe.topic_category',
        'dissertation_category_rel',
        'dissertation_id',
        'category_id',
        string='Tags'
    )

    state = fields.Selection([
        ('draft', 'Draft'),
        ('validated', 'Validated'),
        ('rejected', 'Rejected'),
    ], string="State", default='draft', tracking=True)
    topic_id = fields.Many2one('pfe.topic', string="Topic", required=True, readonly=True)
    supervisor_id = fields.Many2one('hr.employee', string="Supervisor")
    avancement_ids = fields.One2many('pfe.dissertation.avancement', 'dissertation_id', string="Progress")
    group_id = fields.Many2one('pfe.sgroupe', string="Assigned Group")
    choose_id = fields.One2many('pfe.choose_list', 'dissertation_id', string="Choose_list", required=False)
    is_free = fields.Boolean(string="Is Free", default=True, help="Indicates if this dissertation is available for selection.")
    session_id = fields.Many2one('event.event', string="Session", domain="[('is_session', '=', True)]", help="The academic session to which this dissertation belongs.")

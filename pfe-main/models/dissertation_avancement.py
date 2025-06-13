from odoo import models, fields

class DissertationAvancement(models.Model):
    _name = 'pfe.dissertation.avancement'
    _description = 'Dissertation Progress'

    name = fields.Char(string="Progress Title", required=True)
    date = fields.Date(string="Date", required=True)
    progress_percent = fields.Selection([
        ('25', '25%'),
        ('50', '50%'),
        ('75', '75%'),
        ('100', '100%'),], string="Progress (%)", required=True, default='25')

    dissertation_id = fields.Many2one('pfe.dissertation', string="Dissertation", ondelete='cascade')
    stage = fields.Selection([
        ('state_of_art_study', 'State of Art Study'),
        ('data_collection', 'Data Collection'),
        ('design', 'Design '),
        ('implementation', 'Implementation'),
    ], string="Stage", required=True, default='state_of_art_study')

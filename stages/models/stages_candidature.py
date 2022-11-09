from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError


class StagesCandidature(models.Model):
    _name = 'stages.candidature'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Candidatures Stages - طلبات الترشح للتكوين'
    _rec_name = 'name'

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('stages.candidature') or _('New')
        res = super(StagesCandidature, self).create(vals)
        return res

    @api.depends('date_depart', 'date_retour')
    def set_durre(self):
        for rec in self:
            if rec.date_depart:
                if rec.date_retour:
                    if rec.date_retour > rec.date_depart:
                        rec.duree = (rec.date_retour - rec.date_depart).days
                    else:
                        raise UserError(_('La date de retour doit être supérieure à la date de départ'))

    @api.depends('partner_id')
    def set_pays(self):
        for rec in self:
            if rec.partner_id:
                rec.pays = rec.partner_id.country_id.name
            else:
                rec.pays = _("Pays non défini")

    @api.depends('type_stage_id', 'zone', 'duree')
    def set_montant(self):
        for rec in self:
            if rec.type_stage_id:
                obj = self.env['stages.type_stage.indemnite'].search(
                    [('type_stage_id', '=', rec.type_stage_id.name), ('zone_id.name', '=', rec.zone),
                     ('nombre_jour', '=', rec.duree)])
                rec.montant = obj.montant
            else:
                rec.montant = _("Montant non ecnore calculé")

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'
            rec.cause_chg_invisible = True

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

    # def _default_country_id(self):
    #     return self.env.ref('base.DZD').id

    name = fields.Char(string='Référence', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    employee_id = fields.Many2one(comodel_name="hr.employee", string="Enseignant", required=True, )
    nom_prenom_ar = fields.Char(related="employee_id.nom_prenom_ar", string="En lettre arabe", )
    civilite = fields.Char(related="employee_id.civilite.name", string="Civilite", )
    work_email = fields.Char(related='employee_id.work_email', string="Email", readonly=False, related_sudo=False)
    department_id = fields.Char(related="employee_id.department_id.name", string="Département", )
    lab_id = fields.Char(related="employee_id.lab_id.name", string="Laboratoire", )
    grade_id = fields.Char(related="employee_id.grade_id.name", string="Grade scientifique", )
    session_id = fields.Many2one(comodel_name="event.event", string="Session stage", required=True, )
    type_stage_id = fields.Many2one(comodel_name="stages.type_stage", string="Type Stage", required=True,
                                    readonly=True, )
    partner_id = fields.Many2one(comodel_name="res.partner", string="Organisme d'accueil", required=True, )
    pays = fields.Char(compute='set_pays', string="Pays", )
    contact = fields.Char(related="partner_id.child_ids.name", string="Contact", )
    zone = fields.Char(related="partner_id.country_id.country_group_ids.name", string="Zone", )
    state = fields.Selection(string="Etat Candidature", selection=[
        ('draft', 'Brouillon'),
        ('confirm', 'Confirmée'),
        # ('chg_period', 'Période changée'),
        # ('open', 'En cours),
        ('done', 'Réalisée'),
        ('cancel', 'Annulée')], readonly=True, default='draft')
    dernier_stage = fields.Date(string="Date dernier Stage", required=True, )
    date_depart = fields.Date(string="Date de départ", track_visibility='always', required=True, )
    date_retour = fields.Date(string="Date de retour ", track_visibility='always', required=True, )
    duree = fields.Integer(string="Durée", compute='set_durre', store=True, )
    cause_chg_period = fields.Char(string="Cause changement période", track_visibility='always', )
    cause_chg_invisible = fields.Boolean(string="Visibility de Cause changement période", default=True, required=True, )
    currency_id = fields.Many2one('res.currency',
                                  default=lambda self: self.env['res.currency'].search([('name', '=', 'DZD')]).id,
                                  readonly=True)
    # currency_id = fields.Many2one('res.currency', string='Currency', default=_default_country_id, readonly=True)
    montant = fields.Float(string="Montant", compute="set_montant", )
    objectifs_stage = fields.Html(string="Objectifs du stage", default="Entrer les objectifs du stage...", )
    methodologie = fields.Html(string="Méthodologie", default="Entrer votre methodologie...", )
    impacts_attendus = fields.Html(string="Impacts attendus", default="Entrer les impacts attendus...")
    engagement = fields.Boolean(string="Engagement", )
    active = fields.Boolean(string="Active", default=True)
    is_favorite = fields.Boolean(string="Favori", default=False)
    priority = fields.Selection([('0', 'Normal'), ('1', 'Favorite'), ], default='0', string="Favorite")


class StagesCandidaturePerfectionnement(models.Model):
    _name = 'stages.candidature.perfectionnement'
    _inherit = {'stages.candidature'}
    _description = "Stages Perfectionnement - تربص تحسين المستوى بالخارج"

    doc_depart_ids = fields.One2many("stages.docs_depart", "candidature_perfec_id", string="Documents de Départ", )
    doc_retour_ids = fields.One2many("stages.docs_retour", "candidature_perfec_id", string="Documents de Retour", )

    speciality = fields.Char(string="Spéciality", required=False, )
    diplome_prepare = fields.Selection(string="Diplôme préparé",
                                       selection=[('doctorat', 'Doctorat / دكتورا'),
                                                  ('master', 'Master / ماستر'), ], required=False, )
    intitule_these = fields.Char(string="Intitulé de la thèse", required=False, )
    date_1er_inscription = fields.Date(string="Date 1ère inscription", required=False, )
    nbr_inscription = fields.Selection(string="Nbr d'inscription",
                                       selection=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'),
                                                  ('6', '6'), ('+', 'plus de 6'), ], required=False, )
    type_inscription = fields.Selection(string="Type d'inscription",
                                        selection=[('ordinaire', 'Ordinaire / عادية'),
                                                   ('cotutelle ', 'Cotutelle / إشراف مشترك'),
                                                   ('coenadrement', 'Coenadrement / تأطير مشترك'), ], required=False, )


class StagesCandidatureManifestation(models.Model):
    _name = 'stages.candidature.manifestation'
    _inherit = {'stages.candidature'}
    _description = "Manifestation Scientifique - تظاهرة علمية بالخارج"

    doc_depart_ids = fields.One2many("stages.docs_depart", "candidature_manif_id", string="Documents de Départ", )
    doc_retour_ids = fields.One2many("stages.docs_retour", "candidature_manif_id", string="Documents de Retour", )

    speciality = fields.Char(string="Spéciality", required=False, )
    intitule_manifestation = fields.Char(string="Intitulé de la Manifestation", required=False, )
    lien_web = fields.Char(string="Lien web", required=False, )
    nature = fields.Selection(string="", selection=[
        ('orale', 'Présentation orale - شفوية مداخلة'),
        ('poster', 'Poster - ملصقة'),
        ('intervention', ' Intervention - مداخلة'),
        ('autre', 'Autre - شيء اخر'), ], required=False, )


class StagesCandidatureSejour(models.Model):
    _name = 'stages.candidature.sejour'
    _inherit = {'stages.candidature'}
    _description = "Séjour scientifique de haut niveau - إقامة علمية رفيعة المستوى بالخارج"

    doc_depart_ids = fields.One2many("stages.docs_depart", "candidature_sejour_id", string="Documents de Départ", )
    doc_retour_ids = fields.One2many("stages.docs_retour", "candidature_sejour_id", string="Documents de Retour", )

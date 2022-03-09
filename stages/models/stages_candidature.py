from odoo import models, fields, api,  _
from datetime import datetime, timedelta
from odoo.exceptions import UserError


class StagesCandidature(models.Model):
    _name = 'stages.candidature'
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
                     raise UserError('La date de retour doit être supérieure à la date de départ')

    @api.depends('partner_id')
    def _set_pays(self):
        for rec in self:
            if rec.partner_id:
               rec.pays = rec.partner_id.country_id.name

    name = fields.Char(string='Référence', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    employee_id =fields.Many2one(comodel_name="hr.employee", string="Enseignant", required=True,)
    session_id= fields.Many2one(comodel_name="event.event", string="Session Stage", required=True, )
    type_stage_id = fields.Many2one(comodel_name="stages.type_stage", string="Type Stage", required=True, readonly=True,)
    partner_id  = fields.Many2one(comodel_name="res.partner", string="Organisme d'accueil", required=True, )
    # pays = fields.Char(related="partner_id.country_id.name", string="Pays", )
    pays = fields.Char(compute= '_set_pays', string="Pays", )
    contact = fields.Char(related="partner_id.child_ids.name", string="Contact", readonly=False, )
    state = fields.Selection(string="Etat Candidature",selection=[
            ('draft', 'Brouillon'), ('confirm', 'Confirmée'), ('chg_period', 'Période changée'),
            ('done', 'Réalisée'), ('cancel', 'Annulée'), ], readonly=True, default='draft')
    dernier_stage = fields.Date(string="Date dernier Stage", required=True, )
    date_depart = fields.Date(string="Date de départ", required=True, )
    date_retour = fields.Date(string="Date de retour ", required=True, )
    duree = fields.Integer(string = "Durée du Stage", compute= 'set_durre', store=True,)
    # string = "Durée du Stage",
    cause_chg_period = fields.Char(string="Cause changement période", required=False, )
   # montant_bourse = fields.Float(string="Montant bourse",  required=False, )
    montant_bourse = fields.Float(related="type_stage_id.indemnite_stage_ids.montant" ,string="Montant bourse", )
    objectifs_stage = fields.Text(string="Objectifs du stage", required=False, )
    methodologie = fields.Text(string="Méthodologie", required=False, )
    impacts_attendus  = fields.Text(string="Impacts attendus", required=False, )
    engagement = fields.Boolean(string="Engagement", )
    doc_depart_ids = fields.One2many(comodel_name="stages.docs_depart", inverse_name="candidature_id", string="Documents de Départ", required=False, )
    doc_retour_ids = fields.One2many(comodel_name="stages.docs_retour", inverse_name="candidature_id", string="Documents de Retour", required=False, )



class StagesCandidaturePerfectionnement(models.Model):
    _name = 'stages.candidature.perfectionnement'
    _inherits = {'stages.candidature':'candidature_id'}
    _description = "Stages Perfectionnement - تربص تحسين المستوى بالخارج"

    intitule_these = fields.Char(string="Intitulé de la thèse", required=False, )
    date_1er_inscription = fields.Date(string="Date 1ère inscription", required=False, )
    nbr_inscription  = fields.Selection(string="Nbr d'inscription", selection=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),('5', '5'), ('6', '6'),('+', 'plus de 6'),], required=False, )

    candidature_id = fields.Many2one(comodel_name="stages.candidature", string="Candidature", )
    duree_bis = fields.Integer(compute='set_durre', readonly=True, store=False, )
    pays_bis = fields.Char(compute='_set_pays', readonly=True, store=False, )

    @api.depends('date_retour', 'date_depart')
    def set_durre(self):
        for rec in self:
            if rec.date_depart:
                if rec.date_retour:
                    if rec.date_retour > rec.date_depart:
                        rec.duree = (rec.date_retour - rec.date_depart).days
                    else:
                     raise UserError('La date de retour doit être supérieure à la date de départ')

    @api.depends('partner_id')
    def _set_pays(self):
        for rec in self:
            if rec.partner_id:
               rec.pays = rec.partner_id.country_id.name


class StagesCandidatureManifestation(models.Model):
    _name = 'stages.candidature.manifestation'
    _inherits = {'stages.candidature':'candidature_id'}
    _description = "Manifestation Scientifique - تظاهرة علمية بالخارج"

    intitule_manifestation = fields.Char(string="Intitulé de la Manifestation", required=False, )
    lien_web = fields.Char(string="Lien web", required=False, )
    nature = fields.Selection(string="", selection=[
        ('orale', 'Présentation orale - شفوية مداخلة'),
        ('poster', 'Poster - ملصقة'),
        ('intervention', ' Intervention - مداخلة'),
        ('autre', 'Autre - شيء اخر'), ], required=False, )

    candidature_id = fields.Many2one(comodel_name="stages.candidature", string="Candidature", )


class StagesCandidatureSejour(models.Model):
    _name = 'stages.candidature.sejour'
    _inherits = {'stages.candidature':'candidature_id'}
    _description = "Séjour scientifique de haut niveau - إقامة علمية رفيعة المستوى بالخارج"

    candidature_id = fields.Many2one(comodel_name="stages.candidature", string="Candidature - طلب الترشح", )

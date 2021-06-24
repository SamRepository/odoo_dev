from odoo import models, fields, api,  _

class StagesCandidature(models.Model):
    _name = 'stages.candidature'
    _description = 'Candidatures Stages - طلبات الترشح للتكوين'
    _rec_name = 'name'

    name = fields.Char(string="Référence - المرجع", required=True)
    session_id= fields.Many2one(comodel_name="event.event", string="Session Stage - فترة التربص", required=True, )
    type_stage_id = fields.Many2one(comodel_name="stages.type_stage", string="Type Stage - نوع التربص", required=True,)
    state = fields.Selection(string="Etat Candidature",selection=[
            ('draft', 'Brouillon'), ('confirm', 'Confirmée'), ('chg_period', 'Période changée'),
            ('done', 'Réalisée'), ('cancel', 'Annulée'), ], readonly=True, default='draft')
    dernier_stage = fields.Date(string="Date dernier Stage - تاريخ أخر تربص", required=True, )
    date_depart = fields.Date(string="Date de départ - تاريخ الذهاب", required=True, )
    date_retour = fields.Date(string="Date de retour - تاريخ الرجوع ", required=True, )
    duree = fields.Integer(string="Durée du Stage - مدة التربص", required=False, )
    cause_chg_period = fields.Char(string="Cause changement période - سبب تغيير التاريخ", required=False, )
    montant_bourse = fields.Float(string="Montant bourse - قيمة التربص",  required=False, )
    objectifs_stage = fields.Text(string="Objectifs du stage - الهدف من التربص", required=False, )
    Methodologie = fields.Text(string="Méthodologie - المنهجية", required=False, )
    Impacts_attendus  = fields.Text(string="Impacts attendus - التأثيرات المنتظرة", required=False, )
    engagement = fields.Boolean(string="Engagement - تعهد :", )
    doc_depart_ids = fields.One2many(comodel_name="stages.docs_depart", inverse_name="candidature_id", string="Documents de Départ - وثائق الذهاب  ", required=False, )
    doc_retour_ids = fields.One2many(comodel_name="stages.docs_retour", inverse_name="candidature_id", string="Documents de Retour - وثائق الرجوع  ", required=False, )

class StagesCandidaturePerfectionnement(models.Model):
    _name = 'stages.candidature.perfectionnement'
    _inherits = {'stages.candidature':'candidature_id'}
    _description = "Stages Perfectionnement - تربص تحسين المستوى بالخارج"


    intitule_these = fields.Char(string="Intitulé de la thèse - عنوان المذكرة", required=False, )
    annee_1er_inscription = fields.Date(string="Année 1ère Inscription - السنة الأولى للتسجيل", required=False, )
    nbr_inscription = fields.Integer(string="Nombre d'inscription - عدد التسجيلات", required=False, )

    candidature_id = fields.Many2one(comodel_name="stages.candidature", string="Candidature - طلب الترشح", )


class StagesCandidatureManifestation(models.Model):
    _name = 'stages.candidature.manifestation'
    _inherits = {'stages.candidature':'candidature_id'}
    _description = "Manifestation Scientifique - تظاهرة علمية بالخارج"

    intitule_manifestation = fields.Char(string="Intitulé de la Manifestation - عنوان التظاهرة", required=False, )
    lien_web = fields.Char(string="Lien web - الرابط الإلكتروني", required=False, )
    nature = fields.Selection(string="", selection=[
        ('orale', 'Présentation orale - شفوية مداخلة'),
        ('poster', 'Poster - ملصقة'),
        ('intervention', ' Intervention - مداخلة'),
        ('autre', 'Autre - شيء اخر'), ], required=False, )

    candidature_id = fields.Many2one(comodel_name="stages.candidature", string="Candidature - طلب الترشح", )


class StagesCandidatureSejour(models.Model):
    _name = 'stages.candidature.sejour'
    _inherits = {'stages.candidature':'candidature_id'}
    _description = "Séjour scientifique de haut niveau - إقامة علمية رفيعة المستوى بالخارج"

    candidature_id = fields.Many2one(comodel_name="stages.candidature", string="Candidature - طلب الترشح", )

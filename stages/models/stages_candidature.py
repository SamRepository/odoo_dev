from odoo import models, fields, api,  _

class StagesCandidature(models.Model):
    _name = 'stages.candidature'
    _description = 'Candidatures Stages - طلبات الترشح للتكوين'
    _rec_name = 'name'

    name = fields.Char(string="Référence - المرجع", required=True)
    session_id= fields.Many2one(comodel_name="event.event", string="Session Stage - فترة التربص", required=True, )
    type_stage_id = fields.Many2one(comodel_name="stages.type_stage", string="Type Stage - نوع التربص", required=True,)
    state = fields.Selection(string="Etat Candidature",selection=[
            ('draft', 'Brouillon'),
            ('confirm', 'Confirmée'),
            ('chg_period', 'Période changée'),
            ('done', 'Réalisée'),
            ('cancel', 'Annulée'),
        ], readonly=True, default='draft')
    dernier_stage = fields.Date(string="Date dernier Stage - تاريخ أخر تربص", required=True, )
    date_depart = fields.Date(string="Date de départ - تاريخ الذهاب", required=True, )
    date_retour = fields.Date(string="Date de retour - تاريخ الرجوع ", required=True, )
    duree = fields.Integer(string="Durée du Stage - مدة التربص", required=False, )
    cause_chg_period = fields.Char(string="Cause changement période - سبب تغيير التاريخ", required=False, )
    montant_bourse = fields.Float(string="Montant bourse - قيمة التربص",  required=False, )
    cadre_formation = fields.Text(string="Cadre de formation - مشروع العمل", required=False, )
    objectifs_stage = fields.Text(string="Objectifs du stage - الهدف من التربص", required=False, )
    Methodologie = fields.Text(string="Méthodologie - المنهجية", required=False, )
    Impacts_attendus  = fields.Text(string="Impacts attendus - التأثيرات المنتظرة", required=False, )
    engagement = fields.Boolean(string="Engagement - تعهد :", )
    doc_depart_ids = fields.One2many(comodel_name="stages.docs_depart", inverse_name="candidature_id", string="Documents de Départ - وثائق الذهاب  ", required=False, )

class StagesCandidaturePerfectionnement(models.Model):
    # _name = 'stages.candidature.perfectionnement'
    # _inherits = ['stages.candidature']
    #
    # intitule_these = fields.Char(string="Intitulé de la thèse - عنوان المذكرة", required=False, )
    # annee_1er_inscription = fields.Date(string="Année 1ère Inscription - السنة الأولى للتسجيل", required=False, )
    # nbr_inscription = fields.Integer(string="Nombre d'inscription - عدد التسجيلات", required=False, )



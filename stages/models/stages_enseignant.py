# -*- coding: utf-8 -*-

from odoo import models, fields, api,  _

class StagesEnseignant(models.Model):
    _name = 'stages.enseignant'
    _description = 'Enseignant - الاساتذة'
    _rec_name = 'name'

    name = fields.Char(string="Référence - المرجع", required=True)
    num_pers = fields.Char(string="Num Personel - الرقم التعريفي", required=False, )
    civilite = fields.Selection(string="Civilité - الهوية", selection=[('mr', 'Mr - السيد'), ('mme', 'Mme - السيدة'), ('melle', 'Melle - الآنسة'), ], required=True, )
    nom_prenom_fr = fields.Char(string="Nom et Prénom", required=True, )
    nom_prenom_ar = fields.Char(string="اللقب و الاسم", required=True, )
    specialite = fields.Char(string="Spécialité - التخصص", required=False,)
    diplome_actu = fields.Char(string="Diplôme actuel - الشهادة الحالية", required=False,)
    adresse = fields.Text(string="Adresse", required=False, )
    passport_id = fields.Integer(string="Passport ID - رقم جواز السفر",required=False, )
    date_naiss = fields.Date(string="Date de naissance - تاريخ الميلاد", required=False, )
    date_recru = fields.Date(string="Date de recrutement - تاريخ التوظيف", required=False, )
    lieu_naiss = fields.Many2one(comodel_name="res.country.state", string="Lieu de naissance - مكان الميلاد", required=False, )
    tel = fields.Char(string="Téléphone - الهاتف", required=False, )
    email = fields.Char(string="Courrier Électronique - البريد الإلكتروني", required=False, )
    image = fields.Binary(string="Photo - الصورة", attachment=True )
    sexe = fields.Selection([ ('male', 'Male'), ('female', 'Female'), ], default='male', string="Sexe - الجنس")
    active = fields.Boolean(string="Active - مفعل", default=True)

    user_id = fields.Many2one('res.users', string="Utilisateur - إسم المستخدم", required=False,)
    dpte_id = fields.Many2one(comodel_name="stages.departement", string="Département - القسم", required=False, )
    lab_id = fields.Many2one(comodel_name="stages.laboratoire", string="Laboratoire - المخبر", required=False, )
    grade_id = fields.Many2one(comodel_name="stages.grade", string="Grade scientifique - الرتبة العلمية", required=False, )



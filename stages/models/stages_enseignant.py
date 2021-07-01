# -*- coding: utf-8 -*-

from odoo import models, fields, api,  _

class StagesEnseignant(models.Model):
    _inherit = ['hr.employee']

    num_pers = fields.Char(string="Num Personel - الرقم التعريفي", required=False, )
    civilite = fields.Many2one(comodel_name="res.partner.title", string="Civilité - الهوية", required=False, )
#   civilite = fields.Selection(string="Civilité - الهوية", selection=[('mr', 'Mr. - السيد'), ('mme', 'Mme. - السيدة'), ('melle', 'Melle. - الآنسة'),('dr', 'Dr. - الدكتور'), ('pr', 'Pr. - البروفسور'),], required=True, )
    nom_prenom_ar = fields.Char(string=" Nom et prénom -  بالحروف العربية ", required=True, )
    date_recru = fields.Date(string="Date de recrutement - تاريخ التوظيف", required=False, )

    lab_id = fields.Many2one(comodel_name="res.partner", string="Laboratoire - المخبر", required=False, )
    grade_id = fields.Many2one(comodel_name="stages.grade", string="Grade scientifique - الرتبة العلمية", required=False, )

    # specialite = fields.Char(string="Spécialité - التخصص", required=False,)
    # diplome_actu = fields.Char(string="Diplôme actuel - الشهادة الحالية", required=False,)
    # adresse = fields.Text(string="Adresse", required=False, )
    # passport_id = fields.Integer(string="Passport ID - رقم جواز السفر",required=False, )
    # date_naiss = fields.Date(string="Date de naissance - تاريخ الميلاد", required=False, )
    # lieu_naiss = fields.Many2one(comodel_name="res.country.state", string="Lieu de naissance - مكان الميلاد", required=False, )
    # tel = fields.Char(string="Téléphone - الهاتف", required=False, )
    # email = fields.Char(string="Courrier Électronique - البريد الإلكتروني", required=False, )
    # image = fields.Binary(string="Photo - الصورة", attachment=True,  help="Ce champ contient l'image utilisée comme avatar pour cet enseignant ",)
    # sexe = fields.Selection([ ('male', 'Male'), ('female', 'Female'), ], default='male', string="Sexe - الجنس")
    # active = fields.Boolean(string="Active - مفعل", default=True)
    # website = fields.Char(string='Siteweb - الموقع الشخصي')
    # comment = fields.Text(string='Note infos - معلومات إضافية')
    #
    # bank_ids = fields.One2many('res.partner.bank', 'partner_id', string='Comptes Bancaires - الحسابات البنكية')
    # state_id = fields.Many2one("res.country.state", string='Wilaya - الولاية', ondelete='restrict',
    #                            domain="[('country_id', '=?', country_id)]")
    # country_id = fields.Many2one('res.country', string='Paye - البلد', ondelete='restrict')

    # user_id = fields.Many2one('res.users', string="Utilisateur - إسم المستخدم", required=False,)
    # dpte_id = fields.Many2one(comodel_name="stages.departement", string="Département - القسم", required=False, )




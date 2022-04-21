# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
#
# Copyright (c) 2016  - Osis - www.osis-dz.net


from odoo.osv import expression
from odoo import fields, models, api
from odoo.addons import decimal_precision as dp


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    @api.multi
    @api.depends('name', 'first_name')
    def name_get(self):
        result = []
        for hr in self:
            if hr.first_name:
                name = hr.name + ' ' + hr.first_name
            else:
                 name = hr.name
            result.append((hr.id, name))
        return result

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=80):
        """ Returns a list of tupples containing id, name, as internally it is called {def name_get}
            result format: {[(id, name), (id, name), ...]}
        """
        args = args or []
        if operator in expression.NEGATIVE_TERM_OPERATORS:
            domain = [('first_name', operator, name), ('name', operator, name)]
        else:
            domain = ['|', ('first_name', operator, name), ('name', operator, name)]
        name = self.search(expression.AND([domain, args]), limit=limit)
        return name.name_get()

    first_name = fields.Char('First name', required=True)
    matricule  = fields.Char('Registration number')

    address_home = fields.Char('Personal Address')
    housewife  =  fields.Boolean('housewife')
    maiden_name = fields.Char('Maiden name')

    ss = fields.Boolean('Contributes to cnas ?', default=True)
    spouse_name =  fields.Char('Spouse name')
    ss_num  = fields.Char('Cnas number',size=13)
    ss_since =  fields.Date('Since')
    ss_mutual =  fields.Char('Mutual')
    cnas =  fields.Selection([(9,'9%'),
                              (5,'Handicapé 5%'),
                              (7,'Emploi Jeune 7%')],'Cnas', default=9)
    cnasp  = fields.Float('Cotisation Patronale', default=25)
    cnasp1 = fields.Float('Oeuvre Sociale 0.5%', default=0.5)
    cnasp2 = fields.Float('Cot part Logement sociale 0.5%', default=0.5)

    #Rubriques
    ppanier  = fields.Float('Prime de panier')
    ptransport  = fields.Float('Prime de transport')
    itelephone  = fields.Float('Téléphone')
    iuvp = fields.Float('Ind. véhicule personnel')

    iep = fields.Float('Ind. experience professionnelle')
    inuisance_p = fields.Float('Indémnité de nuisance')
    inuisance_m = fields.Float('Indémnité de nuisance')
    ifonction = fields.Float('Indémnité de fonction')
    icaisse = fields.Float('Indémnité de caisse')
    iastreinte = fields.Float('Indémnité de d\'astreinte')

    sunique = fields.Float('Salaire unique')
    echouhadas = fields.Float('Bonification enfants de chouhadas')

    irg_cot_10 = fields.Float('Rubrique Cotisable IRG 10%')
    irg_imp_10 = fields.Float('Rubrique Imposable IRG 10%')







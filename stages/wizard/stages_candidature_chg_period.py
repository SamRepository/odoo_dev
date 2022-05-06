from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError


class ChangePeriodWizard(models.TransientModel):
    _name = 'stages.candidature.chg.period'
    _description = 'Changer Période Candidature'

    @api.model
    def default_get(self, fields):
        res = super(ChangePeriodWizard, self).default_get(fields)
        main_rec = self.env['stages.candidature.perfectionnement'].browse(self.env.context.get('active_id'))
        if 'date_depart' and 'date_retour' in fields:
            res["date_depart"] = main_rec.date_depart
            res["date_retour"] = main_rec.date_retour
            res["cause_chg_period"] = main_rec.cause_chg_period
        return res

    def action_confirm(self):
        for rec in self:
            main_rec = self.env['stages.candidature.perfectionnement'].browse(self.env.context.get('active_id'))
            if main_rec.date_depart != rec.date_depart or main_rec.date_retour != rec.date_retour:
                main_rec.cause_chg_period = rec.cause_chg_period
                main_rec.cause_chg_invisible = False
                main_rec.date_depart = rec.date_depart
                main_rec.date_retour = rec.date_retour
            else:
                raise UserError('Il faut au moins changer la date de départ ou de retour !')

    date_depart = fields.Date(string="Date de départ", required=True, )
    date_retour = fields.Date(string="Date de retour ", required=True, )
    cause_chg_period = fields.Char(string="Cause changement période", required=True, )




    # duree = fields.Integer(string="Durée", compute='set_durre', store=True, )
    # cause_chg_period = fields.Char(string="Cause changement période", required=False, )
    # currency_id = fields.Many2one('res.currency',default=lambda self: self.env['res.currency'].search([('name', '=', 'DZD')]).id, readonly=True)
    # montant = fields.Float(string="Montant", compute="set_montant", )

    # @api.depends('date_depart', 'date_retour')
    # def set_durre(self):
    #     for rec in self:
    #         if rec.date_depart:
    #             if rec.date_retour:
    #                 if rec.date_retour > rec.date_depart:
    #                     rec.duree = (rec.date_retour - rec.date_depart).days
    #                 else:
    #                     raise UserError('La date de retour doit être supérieure à la date de départ')


    # @api.depends('type_stage_id', 'zone', 'duree')
    # def set_montant(self):
    #     for rec in self:
    #         if rec.type_stage_id:
    #             obj = self.env['stages.type_stage.indemnite'].search(
    #             [('type_stage_id', '=', rec.type_stage_id.name), ('zone_id.name', '=', rec.zone),
    #              ('nombre_jour', '=', rec.duree)])
    #             rec.montant = obj.montant
    #         else:
    #             rec.montant = "Montant non ecnore calculé"
    #
    #
    # def action_confirm(self):
    #     for rec in self:
    #         rec.state = 'confirm'
    #
    # def action_cancel(self):
    #     for rec in self:
    #         rec.state = 'cancel'

    # def _default_country_id(self):
    #     return self.env.ref('base.DZD').id


    # @api.model
    # def default_get(self, fields):
    #     res = super(ProductReplenish, self).default_get(fields)
    #     product_tmpl_id = self.env['product.template']
    #     if 'product_id' in fields:
    #         if self.env.context.get('default_product_id'):
    #             product_id = self.env['product.product'].browse(self.env.context['default_product_id'])
    #             product_tmpl_id = product_id.product_tmpl_id
    #             res['product_tmpl_id'] = product_id.product_tmpl_id.id
    #             res['product_id'] = product_id.id
    #         elif self.env.context.get('default_product_tmpl_id'):
    #             product_tmpl_id = self.env['product.template'].browse(self.env.context['default_product_tmpl_id'])
    #             res['product_tmpl_id'] = product_tmpl_id.id
    #             res['product_id'] = product_tmpl_id.product_variant_id.id
    #             if len(product_tmpl_id.product_variant_ids) > 1:
    #                 res['product_has_variants'] = True
    #     company = product_tmpl_id.company_id or self.env.company
    #     if 'product_uom_id' in fields:
    #         res['product_uom_id'] = product_tmpl_id.uom_id.id
    #     if 'company_id' in fields:
    #         res['company_id'] = company.id
    #     if 'warehouse_id' in fields and 'warehouse_id' not in res:
    #         warehouse = self.env['stock.warehouse'].search([('company_id', '=', company.id)], limit=1)
    #         res['warehouse_id'] = warehouse.id
    #     if 'date_planned' in fields:
    #         res['date_planned'] = datetime.datetime.now()
    #     return res
    #
    # def launch_replenishment(self):
    #     uom_reference = self.product_id.uom_id
    #     self.quantity = self.product_uom_id._compute_quantity(self.quantity, uom_reference)
    #     try:
    #         self.env['procurement.group'].with_context(clean_context(self.env.context)).run([
    #             self.env['procurement.group'].Procurement(
    #                 self.product_id,
    #                 self.quantity,
    #                 uom_reference,
    #                 self.warehouse_id.lot_stock_id,  # Location
    #                 _("Manual Replenishment"),  # Name
    #                 _("Manual Replenishment"),  # Origin
    #                 self.warehouse_id.company_id,
    #                 self._prepare_run_values()  # Values
    #             )
    #         ])
    #     except UserError as error:
    #         raise UserError(error)
    #
    # def _prepare_run_values(self):
    #     replenishment = self.env['procurement.group'].create({
    #         'partner_id': self.product_id.with_company(self.company_id).responsible_id.partner_id.id,
    #     })
    #
    #     values = {
    #         'warehouse_id': self.warehouse_id,
    #         'route_ids': self.route_ids,
    #         'date_planned': self.date_planned,
    #         'group_id': replenishment,
    #     }
    #     return values


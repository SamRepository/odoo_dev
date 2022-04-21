# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
#
# Copyright (c) 2022

"""
Calcul IRG.
Realisation : Samir SELLAMI et Toufik Cista - samir.sellami@live.fr
"""
from odoo import api, fields, models
import math


class HrIrg(models.Model):
    _name = 'hr.irg'
    _description = 'Calcul IRG'

    @api.model
    def irg(self, soumis):
        if soumis % 1 == 0:
            aa = int(soumis)
            aa = aa / 10
            soumis = aa * 10
        else:
            soumis = soumis + 0.00000001

        # CALCUL DE L'IMPOT ANNUEL
        rts1 = brts = impota = 0.0
        brts = soumis * 12
        if brts <= 360000.0:
            taux = 0.0
            impan = 0.0
            trs = 360000.0
        elif brts <= 480000.0:
            taux = 23.0
            impan = 0.0
            trs = 240000.0
        elif brts <= 960000.0:
            taux = 27.0
            impan = 55200.0
            trs = 480000.0
        elif brts <= 1920000.0:
            taux = 30.0
            impan = 184800.0
            trs = 960000.0
        elif brts <= 3840000.0:
            taux = 33.0
            impan = 472800.0
            trs = 1920000.0
        elif brts > 3840000.0:
            taux = 35.0
            impan = 1106400.00
            trs = 3840000.0

        # CALCUL DU CREDIT D'IMPOT MENSUEL
        impota = (brts - trs) * taux / 100.0 + impan
        impm = impota / 12.0
        abate = (40.0 * impm / 100.0)
        if abate < 1000.0:
            abate = 1000.0
        if abate > 1500.0:
            abate = 1500.0
        ret = impm - abate
        if ret < 0.0:
            ret = 0.0
        rts1 = ret
        if 360000.0 < brts < 420000.0:
            rts1 = round (rts1 * 137.0 / 51.0 - 27925.0 / 8.0, 2)
            # rts1 = (rts1 * 100.0) + 0.0001
            # rts1 = int(rts1)
            # rts1 = rts1 / 100.0
            return -rts1
        else:
            rts1 = round(rts1, 2)
            rts1 = (rts1 * 100.0) + 0.0001
            rts1 = int(rts1)
            rts1 = rts1 / 100.0
            return -rts1
    #
    # print 'Exemples Pour 32000.00 DA:', irg(32000.00, 32000.00)
    # print '--------  '
    # print 'Exemples Pour 31950.00 DA:', irg(31950.00, 31950.00)
    # print '--------  '
    # print 'Exemples Pour 32120.00 DA:', irg(32120.00, 32120.00)
    # print '--------  '
    # print 'Exemples Pour 340000.0 DA:', irg(340000.00, 340000.00)

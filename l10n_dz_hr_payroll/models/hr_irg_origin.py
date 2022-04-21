# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
#
# Copyright (c) 2016  - Osis - www.osis-dz.net


"""
Calcul IRG.
Realisation : Yacine BENSIDHOUM    yacine.bensidhoum@osis-dz.net
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
        brts = soumis * 12.0

        # if brts <= 120000.0:
        #    taux=0.0
        #    impan=0.0
        #    trs=120000.0

        if brts <= 360000.0:
            taux = 0.0
            impan = 0.0
            trs = 360000.0

        elif brts <= 1440000.0:
            taux = 30.0
            impan = 48000.0
            trs = 360000.0

        elif brts <= 9999999.0:
            taux = 35.0
            impan = 372000.0
            trs = 1440000.0

        elif brts > 9999999.0:
            taux = 35.0
            impan = 3367999.65
            trs = 9999999.0

        # CALCUL DU CREDIT D'IMPOT MENSUEL
        impota = (brts - trs) * taux / 100.0 + impan
        impm = impota / 12.0
        abat = (40.0 * impm / 100.0)
        if abat < 1000.0:
            abat = 1000.0
        if abat > 1500.0:
            abat = 1500.0

        ret = impm - abat
        if ret < 0.0:
            ret = 0.0

        rts1 = math.floor(ret)
        rts1 = (rts1 * 10.0) + 0.0001
        rts1 = int(rts1)
        rts1 = rts1 / 10.0

        return -rts1

    # if __name__=='__main__':
    print ''
    print 'Exemples Pour 119 850.0 DA:', irg(26924.92, 26924.92)
    print '--------  '
    print 'Exemples Pour 50 080.0 DA:', irg(26925.00, 26925.00)
    print '--------  '
    print 'Exemples Pour 30 000.0 DA:', irg(30000.00, 30000.00)
    print '--------  '
    print 'Exemples Pour 15 000.0 DA:', irg(15000.00, 15000.00)

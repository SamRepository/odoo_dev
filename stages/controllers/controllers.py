# -*- coding: utf-8 -*-
from odoo import http

# class Stages(http.Controller):
#     @http.route('/stages/stages/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stages/stages/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('stages.listing', {
#             'root': '/stages/stages',
#             'objects': http.request.env['stages.stages'].search([]),
#         })

#     @http.route('/stages/stages/objects/<model("stages.stages"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stages.object', {
#             'object': obj
#         })
# -*- coding: utf-8 -*-
from odoo import http


class Stages(http.Controller):
    @http.route('/stages/type_stages/', auth='public',website=True)
    def display_stages(self, **kw):
        # return "Hello, world"
        # return "Hello World! Here are the available subjects"
        # return http.request.render('stages.stages_display', {
        #     'stages':
        #         ['Math', 'English', 'Programming', 'Operating System'],
        # })
        stages = http.request.env['stages.type_stage'].search([])
        return http.request.render('stages.stages_display', {
            'stages': stages,
        })

    @http.route('/stages/<model("stages.type_stage"):stage>/', auth='public', website=True)
    def display_stage_detail(self, stage, **kw):
        # grades = http.request.env['stages.grade'].search([])
        return http.request.render('stages.stages_details_display', {
            'stage': stage,
        })

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
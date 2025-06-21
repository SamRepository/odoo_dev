from odoo import http
from odoo.http import request

class DissertationPortal(http.Controller):

    @http.route(['/dissertation/<int:dissertation_id>/add_avancement'], type='http', auth='user', website=True)
    def add_avancement_form(self, dissertation_id, **kwargs):
        dissertation = request.env['pfe.dissertation'].sudo().browse(dissertation_id)
        if not dissertation.exists():
            return request.not_found()
        return request.render('pfe.portal_add_avancement_form', {
            'dissertation': dissertation,
        })

    @http.route(['/dissertation/<int:dissertation_id>/submit_avancement'], type='http', auth='user', website=True, csrf=True)
    def submit_avancement(self, dissertation_id, **post):
        dissertation = request.env['pfe.dissertation'].sudo().browse(dissertation_id)
        if not dissertation.exists():
            return request.not_found()

        request.env['pfe.dissertation.avancement'].sudo().create({
            'name': post.get('title'),
            'date': post.get('date'),
            'progress_percent': post.get('percentage'),
            'stage': post.get('stage'),
            'dissertation_id': dissertation.id,
        })

        return request.redirect('/dissertation/detail/%s' % dissertation_id)


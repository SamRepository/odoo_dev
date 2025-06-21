from odoo import http, fields
from odoo.http import request
import base64

class DissertationPortal(http.Controller):

    @http.route(['/dissertation/<int:dissertation_id>/submit'], type='http', auth='user', website=True)
    def dissertation_submit(self, dissertation_id):
        dissertation = request.env['pfe.dissertation'].sudo().browse(dissertation_id)
        return request.render('pfe.portal_submit_dissertation', {
            'dissertation': dissertation,
        })

    @http.route(['/dissertation/<int:dissertation_id>/submit/upload'], type='http', auth='user', methods=['POST'], website=True, csrf=True)
    def dissertation_upload(self, dissertation_id, **post):
        dissertation = request.env['pfe.dissertation'].sudo().browse(dissertation_id)
        if not dissertation.exists():
            return request.not_found()

        # Utilise request.httprequest.files pour récupérer le fichier
        file = request.httprequest.files.get('submission_file')
        if file:
            dissertation.write({
                'submission_file': base64.b64encode(file.read()),
                'submission_filename': file.filename
            })

        return request.redirect('/dissertation/detail/%s' % dissertation_id)
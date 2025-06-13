from odoo import http
from odoo.http import request


class DefensePortal(http.Controller):
    @http.route(['/defense/upload'], type='http', auth='user', website=True)
    def upload_dissertation_form(self, **kw):
        return request.render('pfe.template_defense_creat', {})

    @http.route(['/defense/submit'], type='http', auth='user', methods=['POST'], website=True, csrf=True)
    def submit_dissertation(self, **post):
        # defense_id = int(post.get('defense_id'))
        dissertation_file = post.get('dissertation_file')
        # New fields
        date = post.get('date')
        time = post.get('time')
        location = post.get('location')
        final_grade = post.get('final_grade')
        comments = post.get('comments')

        if not defense_id or not dissertation_file:
            return request.render('pfe.template_defense_creat', {
                'error': "Please fill in all the required fields."
            })

        defense = request.env['pfe.defense'].sudo().browse(defense_id)
        if not defense.exists():
            return request.render('pfe.template_defense_creat', {
                'error': "Defense not found."
            })

        defense.write({
            'dissertation_file': dissertation_file.read(),
            'dissertation_filename': filename,
            'date': date,
            'time': float(time) if time else 0.0,
            'location': location,
            'final_grade': float(final_grade) if final_grade else 0.0,
            'comments': comments,
        })

        return request.render('pfe.template_defense_creat', {
            'success': True
        })

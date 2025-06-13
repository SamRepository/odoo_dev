from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError
import base64
from werkzeug.utils import secure_filename


class TopicWebsiteController(http.Controller):

    @http.route('/create_topic/', type='http', auth="user", website=True, csrf=True)
    def submit_topic_save(self, **post):
        title = post.get('title')
        description = post.get('description')
        tools = post.get('tools')
        reference = post.get('reference')
        raw_category_ids = request.httprequest.form.getlist('category_ids')

        # معالجة التصنيفات
        existing_ids = []
        new_names = []
        for value in raw_category_ids:
            if value.startswith('new:'):
                new_names.append(value[4:].strip())
            elif value.isdigit():
                existing_ids.append(int(value))

        new_tag_ids = []
        if new_names:
            for name in new_names:
                if name:
                    existing_tag = request.env['pfe.topic_category'].sudo().search([('name', '=ilike', name)], limit=1)
                    if existing_tag:
                        new_tag_ids.append(existing_tag.id)
                    else:
                        new_tag = request.env['pfe.topic_category'].sudo().create({'name': name})
                        new_tag_ids.append(new_tag.id)

        all_tag_ids = existing_ids + new_tag_ids

        # معالجة المرفقات
        attachment_ids = []
        files = request.httprequest.files.getlist('attachments')
        for file in files:
            if file and file.filename:
                data = file.read()
                attachment = request.env['ir.attachment'].sudo().create({
                    'name': secure_filename(file.filename),
                    'datas': base64.b64encode(data),
                    'res_model': 'pfe.topic',
                    'type': 'binary',
                    'mimetype': file.content_type,
                })
                attachment_ids.append(attachment.id)

        try:
            if not title or not description or not tools:
                raise ValidationError("Please fill in all the required fields.")

            employee = request.env.user.employee_id
            request.env['pfe.topic'].sudo().create({
                'title': title,
                'description': description,
                'tools': tools,
                'reference': reference,
                'category_ids': [(6, 0, all_tag_ids)],
                'attachment_ids': [(6, 0, attachment_ids)],
                'supervisor_id': employee.id,
            })

            return request.redirect('/topic/submit/success')

        except Exception as e:
            print("Error while creating topic:", e)
            values = {
                'error': str(e),
                'title': title,
                'description': description,
                'tools': tools,
                'reference': reference,
                'category_ids': request.env['pfe.topic_category'].sudo().search([]),
            }
            return request.render('pfe.topic_submit_templateA', values)

    @http.route('/topic/submit/success', type='http', auth="user", website=True)
    def topic_submit_success(self):
        return request.render('pfe.topic_submit_success')

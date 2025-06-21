from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError

class Choose(http.Controller):

    @http.route('/my/choose', type='http', auth='user', website=True)
    def choose_list(self, **kwargs):
        student = request.env.user.employee_id
        if not student or not student.is_student:
            return request.not_found()

        group = student.group_id

        # ✅ إذا الموضوع راهو متعيّن، نوجه الطالب مباشرة للموضوع ديالو
        if group.selected_dissertation_id:
            return request.redirect('/my/topic')

        dissertations = request.env['pfe.dissertation'].sudo().search([
        ])

        existing_choices = request.env['pfe.choose_list'].search([('group_id', '=', group.id)])
        sequence_range = list(range(1, len(dissertations) + 1))

        return request.render('pfe.choose_list_template1', {
            'group': group,
            'dissertations': dissertations,
            'existing_choices': existing_choices,
            'sequence': sequence_range,
        })

    @http.route('/my/choose/submit/save', type='http', auth='user', methods=['POST'], website=True, csrf=True)
    def choose_submit_save(self, **post):
        try:
            student = request.env.user.employee_id
            if not student or not student.is_student:
                return request.not_found()

            group = student.group_id
            # if not group:
            #     raise ValidationError("You are not assigned to any group.")

            # استخدم httprequest بدلاً من post العادي
            choices = request.httprequest.form.getlist('dissertation_id')
            sequences = request.httprequest.form.getlist('sequence')

            if not choices:
                raise ValidationError("You must choose at least one dissertation.")

            # حذف الخيارات القديمة قبل الحفظ
            request.env['pfe.choose_list'].sudo().search([('group_id', '=', group.id)]).unlink()

            for index, dissertation_id in enumerate(choices):
                sequence = int(sequences[index]) if index < len(sequences) else 0
                if dissertation_id:
                    request.env['pfe.choose_list'].sudo().create({
                        'group_id': group.id,
                        'dissertation_id': int(dissertation_id),
                        'sequence': sequence,
                    })

            return request.render('pfe.choose_success_template', {
                'message': "Your choices have been successfully submitted!", })
        except ValidationError as e:
            return request.render('pfe.topic_submit_templateA', {
                'error': str(e),
            })

    @http.route('/my/topic', type='http', auth='user', website=True)
    def my_topic(self, **kwargs):
        student = request.env.user.employee_id
        if not student or not student.is_student:
            return request.not_found()

        group = student.group_id
        dissertation = group.selected_dissertation_id

        if not dissertation:
            return request.redirect('/my/choose')

        return request.render('pfe.portal_my_topic', {
            'dissertation': dissertation,
        })
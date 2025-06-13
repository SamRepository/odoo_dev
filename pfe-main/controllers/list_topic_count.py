from odoo import http
from odoo import _
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal


class TopicCustomerPortal(CustomerPortal):

    @http.route('/topics/list/', type='http', auth="user", website=True, sitemap=False)
    def portal_topic_list(self, sortby=None, **kw):
        searchbar_sortings = {
            'title': {'label': _('title'), 'order': 'title asc'},
            'state': {'label': _('State'), 'order': 'state asc'},
        }

        if not sortby:
            sortby = 'title'
        order = searchbar_sortings[sortby]['order']

        user_id = request.env.user.id
        topics = request.env['pfe.topic'].sudo().search(
            [('create_uid', '=', user_id), ('state', 'in', ['pending', 'validated'])],
            order=order
        )

        return request.render('pfe.portal_topic_list', {
            'topics': topics,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
            'page_name': 'topic',
        })

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        user_id = request.env.user.id
        values['count_topics'] = request.env['pfe.topic'].sudo().search_count(
            [('create_uid', '=', user_id), ('state', 'in', ['pending', 'validated'])]
        )

        return values

    @http.route('/topic_detail/<model("pfe.topic"):topic>/', type='http',
                auth='user', website=True)
    def topic_detail(self, topic, **kw):
        return http.request.render('pfe.topic_detail',
                                   {'topic': topic, 'page_name': 'topic'})

    @http.route('/topic/edit/<model("pfe.topic"):topic>/', type='http', auth='user', website=True)
    def edit_topic_form(self, topic, **kw):
        if topic.create_uid.id != request.env.user.id:
            raise AccessError("You can only edit your own topics.")
        if topic.state != 'pending':
            raise UserError("Only pending topics can be edited.")
        return request.render('pfe.topic_edit_template', {'topic': topic})

    @http.route('/topic/update/<int:topic_id>/', type='http', auth='user', website=True, csrf=True, methods=['POST'])
    def update_topic(self, topic_id, **post):
        topic = request.env['pfe.topic'].sudo().browse(topic_id)
        if topic.create_uid.id != request.env.user.id:
            raise AccessError("Access denied.")
        if topic.state != 'pending':
            raise UserError("This topic can no longer be edited.")

        topic.sudo().write({
            'title': post.get('title'),
            'description': post.get('description'),
            'tools': post.get('tools'),

        })
        return request.redirect('/topic_detail/%s/' % topic.id)
@http.route('/topic/upload_attachment', type='http', auth='user', methods=['POST'], csrf=False)
def upload_attachment(self, **post):
    topic_id = int(post.get('topic_id'))
    files = request.httprequest.files.getlist('attachments')
    topic = request.env['pfe.topic'].sudo().browse(topic_id)
    for file in files:
        data = base64.b64encode(file.read())
        request.env['ir.attachment'].sudo().create({
            'name': file.filename,
            'datas': data,
            'res_model': 'pfe.topic',
            'res_id': topic.id,
            'type': 'binary',
        })
    return request.redirect('/topic_detail/%s' % topic.id)

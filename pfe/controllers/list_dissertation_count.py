
from odoo import http, _
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal


class DissertationCustomerPortal(CustomerPortal):

    @http.route('/my/dissertation/', type='http', auth="user", website=True, sitemap=False)
    def portal_dissertation_list(self, sortby=None, **kw):
        searchbar_sortings = {
            'title': {'label': _('Title'), 'order': 'topic_id.title asc'},
            'state': {'label': _('State'), 'order': 'topic_id.state asc'},
        }

        if not sortby:
            sortby = 'title'
        order = searchbar_sortings[sortby]['order']

        user_id = request.env.user.id
        employee = request.env['hr.employee'].sudo().search([('user_id', '=', user_id)], limit=1)

        domain = [('topic_id.state', '=', 'validated')]

        if employee and employee.is_student:
            domain.append(('group_id', '=', employee.group_id.id))
        else:
             domain.append(('topic_id.create_uid', '=', user_id))

        dissertations = request.env['pfe.dissertation'].sudo().search(domain)

        return request.render('pfe.portal_dissertation_list', {
            'dissertations': dissertations,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
            'page_name': 'dissertation',
        })

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)

        user_id = request.env.user.id
        employee = request.env['hr.employee'].sudo().search([('user_id', '=', user_id)], limit=1)

        domain = [('topic_id.state', '=', 'validated')]

        if employee and employee.is_student:
            domain.append(('group_id', '=', employee.group_id.id))
        else:
            domain.append(('topic_id.create_uid', '=', user_id))

        values['count_dissertations'] = request.env['pfe.dissertation'].sudo().search_count(domain)

        return values

    @http.route('/dissertation/detail/<model("pfe.dissertation"):dissertation2>/', type='http',
                auth='user', website=True)
    def dissertation_detail1(self, dissertation2, **kw):
        return request.render('pfe.dissertation_detail', {
            'dissertation2': dissertation2,
            'page_name': 'dissertation2',
        })


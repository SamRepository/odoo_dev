from odoo import http, _
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal

class DissertationCustomerPortal(CustomerPortal):
        @http.route('/lists/', type='http', auth="public", website=True, sitemap=False)
        def portal_dissertation_list2(self, sortby=None, **kw):
            searchbar_sortings = {
                'title': {'label': _('title'), 'order': 'title asc'},
                'state': {'label': _('State'), 'order': 'state asc'},
            }

            if not sortby:
                sortby = 'title'
            order = searchbar_sortings[sortby]['order']

            topics = request.env['pfe.topic'].sudo().search([ ('state', '=', 'validated')])

            return request.render('pfe.dissertation_listA', {
                'topics': topics,
                'searchbar_sortings': searchbar_sortings,
                'sortby': sortby,
                'page_name': 'dissertation',
            })

        @http.route('/dissertation_detail/<model("pfe.topic"):topics>/', type='http',
                    auth='public', website=True)
        def topic_detailA(self, topics, **kw):
            return http.request.render('pfe.diss_detail',
                                       {'topic': topics, 'page_name': 'dissertation'})

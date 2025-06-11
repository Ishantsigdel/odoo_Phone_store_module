# controllers/main.py

from odoo import http
from odoo.http import request

class PhoneStoreController(http.Controller):

    @http.route('/phone-store/promotions', type='json', auth="public", website=True)
    def phone_promotions(self):
        phones = request.env['phone.store'].sudo().search([('is_promo', '=', True)], limit=5)
        return [{
            'name': phone.name,
            'price': phone.price
        } for phone in phones]

from odoo import models, fields

class PhoneBrand(models.Model):
    _name = 'phone.brand'
    _description = 'Phone Brand'

    name = fields.Char(string='Brand Name', required=True)
    imei_number = fields.Char(string='IMEI Number', required=True)
    manufactured_year = fields.Date(string='Manufactured Year')
    mrp = fields.Float(string='MRP')
    active = fields.Boolean(string='Active', default=False)


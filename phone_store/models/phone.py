from odoo import models, fields, api

class PhoneStore(models.Model):
    _name = 'phone.store'
    _description = 'Phone Store'

    name = fields.Char(string='Name', required=True)
    phone_number = fields.Char(string='Phone Number', required=True)
    tag_ids = fields.Many2many('phone.tag', string='Tags')

    address = fields.Text(string='Address') 
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string='Gender')
    active = fields.Boolean(string='Active', default=True)
    is_customer = fields.Boolean(string='Customer', default=False)  # Default: Not a customer
    brand_id = fields.Many2one('phone.brand', string='Phone Brand')
    description = fields.Text(string="Description")
    image_1920 = fields.Image(string="Image")

    call_ids = fields.One2many('phone.call', 'store_id', string='Phone calls')

    total_outgoing_cost = fields.Float(string="Total Outgoing Cost", compute="_compute_total_outgoing_cost", store=True)
   
    @api.depends('call_ids.total_cost')
    def _compute_total_outgoing_cost(self):
        for record in self:
            # Sum only 'outgoing' calls
            record.total_outgoing_cost = sum(
                call.total_cost for call in record.call_ids if call.call_type == 'outgoing'
            )


class PhoneCall(models.Model):
    _name = 'phone.call'
    _description = 'Phone Call'

    store_id = fields.Many2one('phone.store', string='Phone Store', required=True)
    name = fields.Char(string='Name')
    call_type = fields.Selection([
        ('incoming', 'Incoming'),
        ('outgoing', 'Outgoing'),
    ], string='Call Type', required=True)

    phone_number = fields.Char(string='Phone Number')
    call_time = fields.Datetime(string='Call Time')

    # Outgoing-specific fields
    time_spent = fields.Float(string='Time Spent (min)')
    cost_per_minute = fields.Float(string='Cost Per Minute')
    total_cost = fields.Float(string='Total Cost', compute='_compute_total_cost', store=True)
    

    @api.depends('time_spent', 'cost_per_minute')
    def _compute_total_cost(self):
        # import pdb;pdb.set_trace()
        for record in self:
            if record.call_type == 'outgoing':
                record.total_cost = record.time_spent * record.cost_per_minute
            else:
                record.total_cost = 0.0

class PhoneTag(models.Model):
    _name = 'phone.tag'
    _description = 'Phone Tag'

    name = fields.Char(string='Tag Name', required=True, translate=True)
    color = fields.Integer(string='Color Index')  # Optional for UI color tag
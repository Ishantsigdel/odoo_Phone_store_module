# from odoo import models, fields, api, _
# from odoo.exceptions import UserError
# from odoo import Command

# class PhoneCall(models.Model):
#     _name = 'phone.call'
#     _description = 'Phone Call'


#     name = fields.Char(string="Call Description", required=True, default="Outgoing Call")

#     store_id = fields.Many2one('phone.store', string="Phone")
#     outgoing = fields.Boolean(string="Is Outgoing?")
#     duration_minutes = fields.Float(string="Duration (Minutes)")
#     cost_per_minute = fields.Float(string="Cost per Minute")
#     total_cost = fields.Float(string="Total Cost", compute="_compute_total_cost", store=True)
#     is_invoiced = fields.Boolean(string="Invoiced", default=False)

#     @api.depends('duration_minutes', 'cost_per_minute')
#     def _compute_total_cost(self):
#         for rec in self:
#             rec.total_cost = rec.duration_minutes * rec.cost_per_minute

#     def action_create_invoice(self):
#         for call in self:
#             if call.is_invoiced:
#                 raise UserError(_("Invoice already created for this call."))

#             if not call.outgoing:
#                 raise UserError(_("Only outgoing calls can be invoiced."))

#             partner = call.store_id.partner_id
#             if not partner:
#                 raise UserError(_("No customer linked to the phone."))

#             invoice = self.env['account.move'].create({
#                 'partner_id': partner.id,
#                 'move_type': 'out_invoice',
#                 'invoice_line_ids': [
#                     Command.create({
#                         'name': f"Call on {call.store_id.name}",
#                         'quantity': 1,
#                         'price_unit': call.total_cost,
#                     })
#                 ]
#             })

#             call.is_invoiced = True
#             call.message_post(body=f"Invoice {invoice.name} created.")

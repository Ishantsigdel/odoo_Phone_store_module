from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo import Command


class PhoneStore(models.Model):
    _name = "phone.store"
    _inherit = ["mail.thread", "mail.activity.mixin"]  # Enable chatter

    _description = "Phone Store"

    name = fields.Char(string="Name", required=True, tracking=True)

    phone_number = fields.Char(string="Phone Number", required=True, tracking=True)
    tag_ids = fields.Many2many("phone.tag", string="Tags", tracking=True)

    address = fields.Text(string="Address", tracking=True)
    gender = fields.Selection(
        [("male", "Male"), ("female", "Female"), ("other", "Other")], string="Gender"
    )
    active = fields.Boolean(string="Active", default=True)
    partner_id = fields.Many2one("res.partner", string="Customer")
    brand_id = fields.Many2one("phone.brand", string="Phone Brand")
    description = fields.Text(string="Description")
    image_1920 = fields.Image(string="Image")

    total_outgoing_cost = fields.Float(
        string="Total Outgoing Cost", compute="_compute_total_outgoing_cost"
    )
    is_invoiced = fields.Boolean(string="Invoiced", default=False)

    call_ids = fields.One2many("phone.call", "store_id", string="Calls")
    invoice_count = fields.Integer(
        string="Invoice Count", compute="_compute_invoice_count"
    )

    status = fields.Selection(
        [
            ("new", "New"),
            ("inprogress", "In Progress"),
            ("completed", "Completed"),
        ],
        default="new",
        string="Status",
        required=True
    )

    # stage_id = fields.Many2one(
    #     "phone.store.stage", string="Stage", group_expand="_read_group_stage_ids"
    # )

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        return self.env["phone.store.stage"].search([])

    # @api.model
    # def _read_group_stage_ids(self, stages, domain, order):
    #     return stages.search([])

    # @api.model
    # def _default_stage_id(self):
    #     return self.env['phone.store.stage'].search([], limit=1).id

    # def _compute_total_outgoing_cost(self):
    #     for record in self:
    #         record.total_outgoing_cost = sum(
    #             call.total_cost for call in record.call_ids if call.call_type == 'outgoing'
    #         )

    def action_view_invoice(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Invoices",
            "res_model": "account.move",
            "view_mode": "tree,form",
            "domain": [
                ("partner_id", "=", self.partner_id.id),
                ("move_type", "=", "out_invoice"),
            ],
            # 'context': "{'create': False}"
        }

    def _compute_invoice_count(self):
        for record in self:
            if record.partner_id:
                record.invoice_count = self.env["account.move"].search_count(
                    [
                        ("partner_id", "=", record.partner_id.id),
                        ("move_type", "=", "out_invoice"),
                    ]
                )
            else:
                record.invoice_count = 0

    def action_create_invoice(self):
        for call in self:
            # if call.is_invoiced:
            #     raise UserError(_("Invoice already created for this call."))

            # if not call.outgoing:
            #     raise UserError(_("Only outgoing calls can be invoiced."))

            partner = call.partner_id
            # if not partner:
            #     raise UserError(_("No customer linked to the phone."))

            invoice = self.env["account.move"].create(
                {
                    "partner_id": partner.id,
                    "move_type": "out_invoice",
                    "invoice_line_ids": [
                        Command.create(
                            {
                                "name": f"Call on {call.name}",
                                "quantity": 1,
                                "price_unit": call.total_outgoing_cost,
                            }
                        )
                    ],
                }
            )

            call.is_invoiced = True
            call.partner_id.message_post(body=f"Invoice {invoice.name} created.")

    @api.depends("call_ids.total_cost")
    def _compute_total_outgoing_cost(self):
        for record in self:
            # Sum only 'outgoing' calls
            record.total_outgoing_cost = sum(
                call.total_cost
                for call in record.call_ids
                if call.call_type == "outgoing"
            )

    #     def action_create_invoice(self):
    #     for call in self:
    #         if call.is_invoiced:
    #             raise UserError(_("Invoice already created for this call."))

    #         if not call.outgoing:
    #             raise UserError(_("Only outgoing calls can be invoiced."))

    #         partner = call.store_id.partner_id
    #         if not partner:
    #             raise UserError(_("No customer linked to the phone."))

    #         invoice = self.env['account.move'].create({
    #             'partner_id': partner.id,
    #             'move_type': 'out_invoice',
    #             'invoice_line_ids': [
    #                 Command.create({
    #                     'name': f"Call on {call.store_id.name}",
    #                     'quantity': 1,
    #                     'price_unit': call.total_cost,
    #                 })
    #             ]
    #         })

    #         call.is_invoiced = True
    #         call.message_post(body=f"Invoice {invoice.name} created.")


class PhoneCall(models.Model):
    _name = "phone.call"
    _description = "Phone Call"

    store_id = fields.Many2one("phone.store", string="Phone Store")
    name = fields.Char(string="Name")
    call_type = fields.Selection(
        [
            ("incoming", "Incoming"),
            ("outgoing", "Outgoing"),
        ],
        string="Call Type",
        required=True,
    )

    phone_number = fields.Char(string="Phone Number")
    call_time = fields.Datetime(string="Call Time")
    time_spent = fields.Float(string="Time Spent (min)")
    cost_per_minute = fields.Float(string="Cost Per Minute")
    total_cost = fields.Float(string="Total Cost", compute="_compute_total_cost")
    duration_minutes = fields.Float(string="Duration (Minutes)")
    is_invoiced = fields.Boolean(string="Invoiced", default=False)

    @api.depends("time_spent", "cost_per_minute")
    def _compute_total_cost(self):
        for record in self:
            if record.call_type == "outgoing":
                record.total_cost = record.time_spent * record.cost_per_minute
            else:
                record.total_cost = 0.0


class PhoneTag(models.Model):
    _name = "phone.tag"
    _description = "Phone Tag"

    name = fields.Char(string="Tag Name", required=True, translate=True)
    color = fields.Integer(string="Color Index")  # Optional for UI color tag


class search(models.Model):
    _inherit = "res.partner"

    def action_view_invoice(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Vehicles",
            "view_mode": "tree",
            "res_model": "fleet.vehicle",
            "domain": [("driver_id", "=", self.id)],
            "context": "{'create': False}",
        }

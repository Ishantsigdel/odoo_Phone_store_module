from odoo import models, fields


class PhoneStoreStage(models.Model):
    _name = "phone.store.stage"
    _description = "Phone Store Stage"
    _order = "sequence, id"

    name = fields.Char(string="Stage Name", required=True)
    sequence = fields.Integer(default=1)
    fold = fields.Boolean(string="Folded in Kanban", default=False)

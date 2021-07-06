from odoo import api, fields, models


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    name_order = fields.Char(related='order_id.name', string='Order Name', readonly=True)
    user_id = fields.Many2one(related='order_id.user_id', string='Purchase Representative', readonly=True)
    invoice_status = fields.Selection(related='order_id.invoice_status', string='Billing Status', readonly=True)
    origin = fields.Char(related='order_id.origin', string='Source Document', readonly=True)
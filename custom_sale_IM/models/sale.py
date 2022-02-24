# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    employee_id = fields.Many2one('hr.employee', string="Maker")


    @api.onchange('order_line')
    def assign_employee(self):
        for order in self.order_line:
            if order.order_id:
                order.order_id.employee_id = order.employee_id



class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    employee_id = fields.Many2one('hr.employee', string="Maker")

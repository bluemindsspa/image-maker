# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    employee_id = fields.Many2one('hr.employee', string="Maker")
    employee = fields.Char(string="Maker")


    @api.onchange('order_line')
    def assign_employee(self):
        empleados = []
        for order in self.order_line:
            if order.employee_id:
                empleados.append(order.employee_id.name)
                self.employee = empleados



class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    employee_id = fields.Many2one('hr.employee', string="Maker")

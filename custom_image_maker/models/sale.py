# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    solid = fields.Boolean('SOLID')
    srv_start_date = fields.Date('Fecha de inicio de servicios')
    srv_end_date = fields.Date('Fecha de inicio de servicios')
    percentage = fields.Float("Porcentaje")
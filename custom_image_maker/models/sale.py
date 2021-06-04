# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    solid = fields.Boolean('BEST ESTIMATE')
    srv_start_date = fields.Date('Fecha estimada de inicio')
    srv_end_date = fields.Date('Fecha fin de servicios')
    percentage = fields.Float("Porcentaje")
    validate = fields.Boolean('Validar')
    estado = fields.Selection(selection=[
        ('solid', 'Solid'),
        ('stretch', 'Stretch'),
        ('best', 'Best Case')
    ])

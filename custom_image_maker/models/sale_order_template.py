from odoo import api, fields, models

class SaleOrderTemplate(models.Model):
    _inherit = 'sale.order.template'

    is_project = fields.Boolean('Es plantilla de proyecto')

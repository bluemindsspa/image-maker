from odoo import api, fields, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_a_project = fields.Boolean('Para proyecto')

from odoo import api, fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    discount_levels = fields.Boolean(string='Niveles de descuentos', related="company_id.discount_levels", readonly=False)
    discount_level = fields.Float(string='Niveles de descuentos', related="company_id.discount_level", readonly=False)

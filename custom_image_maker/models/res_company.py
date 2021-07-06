from odoo import api, fields, models

class ResCompany(models.Model):
    _inherit = 'res.company'

    discount_levels = fields.Boolean(string='Dicount_leves', default=False)
    discount_level = fields.Float(string='Discount levels')

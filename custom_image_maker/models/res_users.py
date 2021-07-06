from odoo import api, fields, models

class ResUsers(models.Model):
    _inherit = 'res.users'

    approve_discount = fields.Float(string='Importe Aprob. Desc.')
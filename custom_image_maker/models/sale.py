# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    solid = fields.Boolean('BEST ESTIMATE')
    srv_start_date = fields.Date('Fecha estimada de inicio')
    srv_end_date = fields.Date('Fecha fin de servicios')
    percentage = fields.Float("Porcentaje")
    validate = fields.Boolean('Validar', default=False)
    discount_validate = fields.Boolean('Validar Desc.', compute="_compute_discount_validate", store=True)
    lock = fields.Boolean(string='Lock', compute="_compute_lock_validate")
    higher_discount = fields.Float('Higher', compute="_compute_discount_validate", store=True)
    estado = fields.Selection(selection=[
        ('solid', 'Solid'),
        ('stretch', 'Stretch'),
        ('best', 'Best Case')
    ])
    periodo = fields.Integer('Período')
    imteam_id = fields.Many2one('sale.imteam', string='Equipo')

    def _compute_lock_validate(self):
        for rec in self:
            lock = True
            amount_user = self.env.user.approve_discount
            if amount_user:
                if rec.higher_discount <= amount_user:
                    lock = False
            rec.lock = lock

    @api.depends('order_line')
    def _compute_discount_validate(self):
        for rec in self:
            discount_validate = False
            higher = 0.0
            amount_company = self.env.company.discount_level
            if rec.order_line:
                line_discount = rec.order_line.mapped('discount')
                line_discount.sort(reverse=True)
                if line_discount:
                    higher = line_discount[0]
                    if higher > amount_company:
                        discount_validate = True
            rec.higher_discount = higher
            rec.validate = False
            rec.discount_validate = discount_validate

class SaleTeam(models.Model):
    _name = 'sale.imteam'
    _description = 'Equipo de trabajo'

    name = fields.Char('Nombre')
    # order_id = fields.Many2one('Sale Order')
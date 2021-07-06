# -*- coding: utf-8 -*-
from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    count_sale_order = fields.Integer(
        string="Contador",
        required=False,
        compute='cantidad_sale_order')
    recruitment_ids = fields.One2many(
        'hr.job',
        'proposal_reference_id', string="Solicitud")

    def view_sale_order(self):
        res = self.env["ir.actions.act_window"]._for_xml_id('hr_recruitment.action_hr_job')
        res['domain'] = [
            ('proposal_reference_id', '=', self.id)
        ]
        res['context'] = {
            'default_proposal_reference_id': self.id,
        }
        return res

    def cantidad_sale_order(self):
        for sale in self:
            sale.count_sale_order = len(sale.recruitment_ids)

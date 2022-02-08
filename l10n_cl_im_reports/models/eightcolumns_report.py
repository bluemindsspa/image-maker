# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, api, _
from collections import OrderedDict


class CL8ColumnsReport(models.AbstractModel):
    _inherit = "account.eightcolumns.report.cl"

    @api.model
    def _get_lines(self, options, line_id=None):
        res = super(CL8ColumnsReport, self)._get_lines(options, line_id)
        res[-2]['name'] = 'Utilidad del Ejercicio'
        return res
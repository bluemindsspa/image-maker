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

    @api.model
    def _get_templates(self):
        templates = super(CL8ColumnsReport, self)._get_templates()
        templates['main_table_header_template'] = 'l10n_cl_im_reports.main_table_header_eightcolumns'
        return templates

    def _get_columns_name(self, options):
        columns = [
            {'name': _("Cuenta")},
            {'name': _("Débito"), 'class': 'number'},
            {'name': _("Crédito"), 'class': 'number'},
            {'name': _("Deudor"), 'class': 'number'},
            {'name': _("Acreedor"), 'class': 'number'},
            {'name': _("Activo"), 'class': 'number'},
            {'name': _("Pasivo"), 'class': 'number'},
            {'name': _("Perdida"), 'class': 'number'},
            {'name': _("Ganancia"), 'class': 'number'}
        ]
        return columns
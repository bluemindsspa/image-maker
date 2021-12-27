# -*- coding: utf-8 -*-
from odoo import fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'


    def _get_name_invoice_report(self):
        self.ensure_one()
        if self.l10n_latam_use_documents and self.company_id.country_id.code == 'CL':
            return 'report_IM.report_invoice_document'
        return super()._get_name_invoice_report()

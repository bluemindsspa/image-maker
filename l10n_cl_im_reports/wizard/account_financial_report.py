import base64
import xlwt
import time
from odoo import _, api, fields, models
from io import BytesIO
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from odoo.tools.misc import get_lang
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class AccountPrintJournal(models.TransientModel):
    _inherit = "account.print.journal"

    def check_report_xls(self):
        self.ensure_one()
        data = {}
        data['ids'] = self.env.context.get('active_ids', [])
        data['model'] = self.env.context.get('active_model', 'ir.ui.menu')
        data['form'] = self.read([
            'date_from', 'date_to', 'journal_ids', 'target_move', 'company_id', 'sort_selection', 'amount_currency'])[0]
        used_context = self._build_contexts(data)
        data['form']['used_context'] = dict(used_context, lang=get_lang(self.env).code)
        return data

    def export_report_xls(self):
        report_name = 'Auditoría de diarios'
        company = self.env.user.company_id
        data = self.check_report_xls()
        datas = self.env['report.account.report_journal'].sudo()._get_report_values(None, data)
        lines = datas.get('lines')
        docs = datas.get('docs')
        company_id = datas.get('company_id')
        sort_selection = data['form'].get('sort_selection')
        target_move = data['form']['target_move']
        sum_debit = datas.get('sum_debit')
        sum_credit = datas.get('sum_credit')
        get_taxes = datas.get('get_taxes')
        workbook = xlwt.Workbook(encoding="utf-8")
        bold = xlwt.easyxf('font: bold on;')

        for o in docs:
            i = 0
            data['form'].get('sort_selection') == 'move_name'
            sheet = workbook.add_sheet(o.name)
            sheet.write(0, 0, company.name, bold)
            sheet.write(0, 1, 'Fecha: ' + datetime.strftime(fields.Date.context_today(self), '%d/%m/%Y'))
            sheet.write(1, 0, company.l10n_cl_activity_description, bold)
            sheet.write(2, 0, company.partner_id.vat, bold)
            sheet.write(3, 0, report_name, bold)

            sheet.write(6, 0, o.name, bold)
            sheet.write(7, 0, 'Empresa:', bold)
            sheet.write(7, 2, 'Libro:', bold)
            sheet.write(7, 4, 'Asientos ordenados por:', bold)
            sheet.write(7, 6, 'Movimientos del objetivo:', bold)
            sheet.write(8, 0, company_id.name)
            sheet.write(8, 2, o.name)
            sheet.write(8, 4, 'Número de asiento' if sort_selection == 'move_name' else 'Fecha')
            sheet.write(8, 6, 'Todos los asientos' if sort_selection == 'all' else 'Todos los asientos validados')

            taxes = get_taxes(data, o)
            i = 10
            sheet.write(i, 0, 'Asiento', bold)
            sheet.write(i, 1, 'Fecha', bold)
            sheet.write(i, 2, 'Cuenta', bold)
            sheet.write(i, 3, 'Empresa', bold)
            sheet.write(i, 4, 'Etiqueta', bold)
            sheet.write(i, 5, 'Débito', bold)
            sheet.write(i, 6, 'Crédito', bold)
            i += 1
            for aml in lines[o.id]:
                sheet.write(i, 0, aml.move_id.name)
                sheet.write(i, 1, aml.date)
                sheet.write(i, 2, aml.account_id.code)
                sheet.write(i, 3, aml.sudo().partner_id and aml.sudo().partner_id.name and aml.sudo().partner_id.name[:23] or '')
                sheet.write(i, 4, aml.name and aml.name[:35])
                sheet.write(i, 5, aml.debit)
                sheet.write(i, 6, aml.credit)
                i += 1
            i += 2

            sheet.write(i, 4, 'Total:', bold)
            sheet.write(i, 5, sum_debit(data, o), bold)
            sheet.write(i, 6, sum_debit(data, o), bold)

            i += 1
            sheet.write(i, 0, 'Declaración de impuestos', bold)
            i += 1
            sheet.write(i, 0, 'Nombre', bold)
            sheet.write(i, 1, 'Importe base', bold)
            sheet.write(i, 2, 'Importe del impuesto', bold)

            for tax in taxes:
                i += 1
                sheet.write(i, 0, tax.name)
                sheet.write(i, 1, taxes[tax]['base_amount'])
                sheet.write(i, 2, taxes[tax]['tax_amount'])
            i += 4

        fp = BytesIO()
        workbook.save(fp)
        fp.seek(0)
        data = fp.read()
        fp.close()
        data_b64 = base64.encodebytes(data)
        attach = self.env['ir.attachment'].create({
            'name': '%s.xls' % (report_name),
            'type': 'binary',
            'datas': data_b64,
        })
        return {
            'type': "ir.actions.act_url",
            'url': "web/content/?model=ir.attachment&id=" + str(
                attach.id) + "&filename_field=name&field=datas&download=true&filename=" + str(attach.name),
            'target': "self",
            'no_destroy': False,
        }
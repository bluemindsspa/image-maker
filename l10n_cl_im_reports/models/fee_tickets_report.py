# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models, api, _
from collections import OrderedDict


class FeeTicketsReport(models.AbstractModel):
    _name = "account.feetickets.report.cl"
    _inherit = "account.report"
    _description = "Chilean Accounting fee tickets report"

    # filter_date = {'mode': 'range', 'filter': 'this_year'}
    filter_date = {'mode': 'range', 'filter': 'this_month'}
    filter_journals = None
    filter_all_entries = None
    # filter_analytic = False
    filter_multi_company = None

    def _get_report_name(self):
        return _("Libro de Honorarios")

    def _prepare_header_data(self, options):
        company = self.env.company
        return {
            'date_created': fields.Date.today(),
            'date_from': options['date']['date_from'],
            'date_to': options['date']['date_to'],
            # 'Razón Social': company.name,
            # 'R.U.T.': company.vat,
            # 'Dirección': company.currency_id.name,
        }

    def _get_columns_name(self, options):
        columns = [
            {'name': ''},
            # {'name': _("Tipo")},
            {'name': _("Fecha"), 'class': 'date'},
            {'name': _("Correl."), 'class': 'number'},
            {'name': _("N°"), 'class': 'number'},
            {'name': _("Rut")},
            {'name': _("Nombre")},
            {'name': _("Glosa")},
            {'name': _("Bruto"), 'class': 'number'},
            {'name': _("%"), 'class': 'number'},
            {'name': _("Retencion"), 'class': 'number'},
            {'name': _("Total"), 'class': 'number'}
        ]
        return columns

    @api.model
    def _prepare_query(self, options):
        query = """
        SELECT
            move.id AS move_id,
            move.invoice_date AS date,
            move.name as nro,
            partner.vat AS partner_vat,
            COALESCE(partner.name, commercial_partner.name) AS partner_name,
            move.narration as glosa,
            move.amount_untaxed AS bruto,
            act.amount * -1 AS porcent,
            move.amount_tax * -1 AS ret,
            move.amount_total AS total
        FROM account_move move
            LEFT JOIN res_partner partner ON move.partner_id = partner.id
            LEFT JOIN res_partner commercial_partner ON move.commercial_partner_id = commercial_partner.id
            LEFT JOIN account_move_line aml ON move.id = aml.move_id
            LEFT JOIN account_tax act ON aml.tax_line_id = act.id
            INNER JOIN account_journal journal ON journal.id = move.journal_id
        WHERE
            move.state = 'posted'
        AND move.move_type = 'in_invoice'
        AND journal.code = 'BHO'
        AND act.amount <> 0
        AND COALESCE(move.date) BETWEEN %s AND %s
        GROUP by act.amount, move.id, move.invoice_date, move.name, partner.vat, partner_name, move.narration, move.amount_untaxed, move.amount_total
        ORDER by act.amount
        """
        # Date range
        params = [options['date']['date_from'], options['date']['date_to']]

        # Filter on selected journals
        # journal_ids = self.env['account.journal'].search([('type', 'in', ('sale', 'purchase'))]).ids
        # if options.get('journals'):
        #     journal_ids = [c['id'] for c in options['journals'] if c.get('selected')] or journal_ids
        # params.append(tuple(journal_ids))

        return query, params

    @api.model
    def _get_lines(self, options, line_id=None):
        lines = []
        sql_query, parameters = self._prepare_query(options)
        self.env.cr.execute(sql_query, parameters)
        results = self.env.cr.dictfetchall()
        list_percents = [r['porcent'] for r in results]
        percents = []
        for item in list_percents:
            if item not in percents:
                percents.append(item)
        correl = 0
        for p in percents:
            for line in results:
                if line['porcent'] == p:
                    move_id = self.env['account.move'].browse(line['move_id'])
                    # ret = move_id.invoice_line_ids[0].tax_ids[0].filtered(lambda line: 'Impuestos' in line.tax_group_id.name)
                    ret_percent = [l.amount for l in move_id.invoice_line_ids[0].tax_ids if l.tax_group_id.name == 'Impuestos']
                    percent = ret_percent[0] * -1 if ret_percent else 0.00
                    ret = move_id.amount_by_group[0][1] if move_id.amount_by_group else 0
                    line['ret'] = ret
                    invoice_line = move_id.invoice_line_ids
                    # percent = move_id.invoice_line_ids[0].tax_ids[0].amount
                    correl += 1
                    lines.append({
                        'id': line['move_id'],
                        'name': line['nro'],
                        'title_hover': line['nro'],
                        'level': 3,
                        'unfoldable': False,
                        'unfolded': False,
                        # 'colspan': 4,
                        'class': 'o_account_reports_totals_below_sections' if self.env.company.totals_below_sections else '',
                        # 'caret_options': 'account.move.line',
                        # 'parent_id': line['move_id'],
                        'columns': [
                            {'name': values} for values in [
                                # line['tipo'],
                                line['date'],
                                correl,
                                line['nro'],
                                line['partner_vat'],
                                line['partner_name'],
                                invoice_line[0].name,
                                self.format_value(line['bruto']),
                                line['porcent'] or 0.00,
                                self.format_value(ret * -1),
                                self.format_value(line['total'])
                            ]
                        ],
                    })
            if lines:
                totals = self._calculate_totals_perline(results, p)
                lines.append({
                    'id': 'totals_line',
                    'class': 'total',
                    'name': _("Total ") + str(p) + '%',
                    'level': 3,
                    'columns': [
                        {'name': values} for values in [
                            '', '', '', '', '',  '',
                            self.format_value(totals['bruto']),  '',
                            self.format_value(totals['ret'] * -1),
                            self.format_value(totals['total'])
                        ]
                    ],
                    'unfoldable': False,
                    'unfolded': False
                })
        if lines:
            totals = self._calculate_totals(results)
            lines.append({
                'id': 'totals_line',
                'class': 'total',
                'name': _("Total General"),
                'level': 3,
                'columns': [
                    {'name': values} for values in [
                        '', '', '', '', '',  '',
                        self.format_value(totals['bruto']),  '',
                        self.format_value(totals['ret'] * -1),
                        self.format_value(totals['total'])
                    ]
                ],
                'unfoldable': False,
                'unfolded': False
            })
        return lines

    def _calculate_totals(self, lines):
        totals = OrderedDict([
            ('bruto', 0),
            ('ret', 0),
            ('total', 0)
        ])
        for key in totals.keys():
            for line in lines:
                totals[key] += line[key]
        return totals

    def _calculate_totals_perline(self, lines, percent):
        totals = OrderedDict([
            ('bruto', 0),
            ('ret', 0),
            ('total', 0)
        ])
        for key in totals.keys():
            for line in lines:
                if line['porcent'] == percent:
                    totals[key] += line[key]
        return totals

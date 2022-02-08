# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Chile - Accounting Reports',
    'version': '1.1',
    'category': 'Accounting/Localizations/Reporting',
    'author': "Blueminds",
    'website': "blueminds.cl",
    'contributors': ["Boris Silva <silvaboris@gmail.com>"],
    'description': """
        Accounting reports for Chile
        Libro de Honorarios
    """,
    'depends': [
        'account', 'account_reports', 'l10n_cl_reports',
    ],
    'data': [
        # 'security/ir.model.access.csv',
        'views/fee_tickets_report_view.xml',
        'views/report_financial.xml',
    ],
}

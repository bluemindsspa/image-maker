# -*- coding: utf-8 -*-

{
    'name': 'Report invoice export',
    'version': '0.1',
    'category': '',
    'summary': '',
    'description': '',
    'depends': [
        'base',
        'account',
        'report_IM',
        'l10n_cl',
        'l10n_cl_edi',
    ],
    'data': [
        'views/assets.xml',
        'views/layout.xml',
        'views/report_invoice_exportacion.xml',
    ],
    'installable': True,
    'auto_install': False,
}

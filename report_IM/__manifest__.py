# -*- coding: utf-8 -*-

{
    'name': 'Report invoice',
    'version': '0.1',
    'category': '',
    'summary': '',
    'description': '',
    'depends': [
        'base',
        'account',
        'l10n_cl',
        'l10n_cl_edi',
    ],
    'data': [
        'views/assets.xml',
        'views/report_invoice.xml',
    ],
    'installable': True,
    'auto_install': False,
}

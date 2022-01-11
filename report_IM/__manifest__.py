# -*- coding: utf-8 -*-

{
    'name': 'Report invoice',
    'version': '14.0.0.0.1',
    'category': 'Localization/Chile',
    'summary': 'Reporte de Facturación Electrónica para Chile.',
    'author': 'Blueminds',
    'contributors': 'Gabriela Paredes <isabelgpb21@gmail.com>',
    'website': 'https://blueminds.cl',
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

# -*- coding: utf-8 -*-

{
    'name': 'Report invoice export',
    'version': '14.0.0.0.1',
    'category': 'Localization/Chile',
    'summary': 'Reporte de Facturación Electrónica para Chile.',
    'author': 'Blueminds',
    'contributors': 'Gabriela Paredes <isabelgpb21@gmail.com>',
    'website': 'https://blueminds.cl',
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
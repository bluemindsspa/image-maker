# -*- encoding: utf-8 -*-

{
    'name' : 'Libros de Compra y Venta',
    'version' : '1.0',
    'category': 'Custom',
    'description': """reporte de compra y venta, facturando""",
    'author': 'Blueminds',
    'contribuitors': 'Frank Quatromani <fquatromani@blueminds.cl>',
    'website': '',
    'depends' : ['account'],
    'data' : [
        "security/ir.model.access.csv",
        "wizard/account_book_report_views.xml",
    ],
    'installable': True,
    'certificate': '',
}
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Niveles de aprobación para Compras',
    'version': '0.1',
    'category': 'Uncategorized',
    'summary': 'Diferentes niveles de aprobación de compras',
    'description': 'Diferentes niveles de aprobación de compras',
    'author': "Blueminds",
    'website': "http://blueminds.cl",
    'contribuitors': "Frank Quatromani <fquatromani@blueminds.cl>",
    'depends': [
        'purchase'
    ],
    'data': [
        'security/security.xml',
        'views/purchase_views.xml'
    ],
    'installable': True,
    'auto_install': False,
}

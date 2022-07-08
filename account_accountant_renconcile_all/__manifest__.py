# -*- coding: utf-8 -*-
{
    'name': 'Account - Renconcile all Lines',
    'version': '14.0.1.0.0',
    'summary': 'Renconcile all Lines',
    'description': 'Renconcile all Lines',
    'category': '',
    'author': 'Blueminds',
    'website': "blueminds.cl",
    'license': 'LGPL-3',
    'contributors': [
        'Luis Cartaya <luiscartaya653@gmail.com>',
    ],
    'depends': [
        'account', 'account_accountant'
    ],
    'data': [
        'views/assets.xml',
    ],
    'qweb': [
        'static/src/xml/account_reconciliation.xml',
    ],
    'installable': True,
}
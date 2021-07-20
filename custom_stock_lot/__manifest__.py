# -*- coding: utf-8 -*-
{
    'name': "custom_stock_lot",
    'category': 'Stock',
    'version': '14.0.1.0.0',
    'depends': ['base','stock','hr'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/res_config_view_inherit.xml',
    ],
    'demo': [
        #'demo/demo.xml',
    ],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}

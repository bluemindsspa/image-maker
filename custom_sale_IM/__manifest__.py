# -*- coding: utf-8 -*-
{
    'name': "custom_sale_IM",
    'category': 'sale',
    'version': '14.0.1.0.0',
    'depends': ['base','sale','hr', 'custom_image_maker'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/sale_views.xml',
        # 'views/res_config_view_inherit.xml',
    ],
    'demo': [
        #'demo/demo.xml',
    ],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}

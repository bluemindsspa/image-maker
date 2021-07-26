# -*- coding: utf-8 -*-
{
    'name': "Custom Image-Maker",

    'summary': """
        """,

    'description': """
Adecuaciones varias a solicitud
===============================

Se crean campos varios en cabecera de orden de venta:
-----------------------------------------------------

""",

    'author': "Blueminds",
    'website': "blueminds.cl",
    'contributors': ["Boris Silva <silvaboris@gmail.com>"],

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sale',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'sale_management', 'product'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/res_config_settings_views.xml',
        'views/res_users_views.xml',
        'views/product_template_views.xml',
        'views/sale_view.xml',
        'views/sale_order_template_views.xml',
        'report/sale_report_templates.xml',
        # 'views/purchase_views.xml',
    ],

}

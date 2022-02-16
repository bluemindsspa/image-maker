# -*- coding: utf-8 -*-
{
    'name': "Recruiment",

    'summary': """
        """,

    'description': """
    """,

    'author': "Blueminds",
    'website': "blueminds.cl",
    'contributors': [""],
    'category': '',
    'version': '0.1',
    'depends': ['base', 'hr', 'hr_recruitment', 'sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/recruitment_applications.xml',
        'views/type_of_project.xml',
        'views/account_item.xml',
        'views/location.xml',
        'views/type_of_opportunities.xml',
        'views/length_of_service.xml',
        'views/income_ceiling.xml',
        'views/languages.xml',
        # 'views/exclusive_technical_requirements.xml',
        'views/country_search.xml',
        'views/rol.xml',
        'views/sale_views.xml',
        'views/application_status.xml',
    ],

}

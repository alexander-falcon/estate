# -*- coding: utf-8 -*-
{
    'name': "estate",
    'summary': """Real Estate""",
    'depends': ['base'],
    'category': 'Brokerage',
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/property_offer_views.xml',
        'views/property_type_views.xml',
        'views/property_tag_views.xml',
        'views/users.xml',
        'views/estate_menus.xml',
        #'data/estate.property.type.csv',
        'report/estate_report_templates.xml',
        'report/estate_report_views.xml',
    ],
    'demo': [
        #'demo/demo_data.xml',
        "demo/estate_demo.xml"
    ],
    'installable': True,
    'application': True,
} 

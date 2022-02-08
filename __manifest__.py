# -*- coding: utf-8 -*-
{
    'name': "estate",
    'summary': """Real Estate""",
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/property_offer_views.xml',
        'views/property_type_views.xml',
        'views/property_tag_views.xml',
        'views/users.xml',
        'views/estate_menus.xml'
    ],
    'installable': True,
    'application': True,
} 

# -*- coding: utf-8 -*-
{
    'name': "Open Academy",

    'summary': """
        Manage trainings""",

    'description': """
        Es una pruebaa
    """,

    'author': "INTN",
    'website': "http://www.intn.gov.py",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Test',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','board'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        
      
        'views/templates.xml',
        'views/openacademy.xml',
        'views/partner.xml',
        'reports/reports.xml',
        'views/session_board.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
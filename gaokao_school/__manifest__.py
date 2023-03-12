# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "school for Gaokao",

    'summary': "school for Gaokao",

    'description': """
    Schools
    """,

    'category': 'Gaokao/',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'web'],
    'installable': True,
    'application': True,
    'auto_install': False,
    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/school_actions.xml',
        'views/province_actions.xml',
        'views/province_control_actions.xml',
        'views/school_score_actions.xml',
        'views/sp_score_actions.xml',
        'views/oneone_section_actions.xml',
        'views/menu.xml',
    ],
    'assets': {
        'web.assets_backend': [
        #    'gaokao_school/static/src/views/*.js',
        #    'gaokao_school/static/src/views/*.xml',
        ],
    },
    'license': 'OEEL-1',
}

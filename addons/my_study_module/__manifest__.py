{
    'name': "My Study Module",
    'summary': "Sample module for studying Odoo: a simple Study Note model",
    'description': """
Study Notes
===========
A minimal custom module with one model (study.note), list/form views,
a menu item and access rights.
    """,
    'author': "Me",
    'category': 'Tools',
    'version': '20.0.1.0.0',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'security/ir.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
    'installable': True,
}

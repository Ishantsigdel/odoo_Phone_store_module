{
    'name': 'Phone Store',
    'version': '1.0',
    'summary': 'Manage phone numbers',
    'description': 'Simple CRUD system for storing phone numbers.',
    'author': 'Ishant Sigdel',
    'category': 'Tools',
    'depends': ['base', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/brand_views.xml',
        'views/phone_views.xml',
        'views/tags.xml',
        'views/phone_call_views.xml'
    ],
    'installable': True,
    'application': True,
}

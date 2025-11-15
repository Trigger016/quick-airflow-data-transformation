{
    'name': "Open Academy",
    'summary': "Free learning platform with multiple Course",
    'description': """An extra assessment test for M+Software""",
    'author': "farhan.andika",
    'website': "",
    'category': 'Services',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/academy_existing_course.xml',
        'views/courses.xml',
        'views/sessions.xml',
        'views/partners.xml',
        'views/navigation.xml',
    ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
    "installable": True,
    "application": True,
    "auto_install": False,
} # type: ignore


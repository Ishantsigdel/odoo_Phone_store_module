{
    "name": "Phone Store",
    "version": "1.0",
    "summary": "Manage phone numbers",
    "description": "Simple CRUD system for storing phone numbers.",
    "author": "Ishant Sigdel",
    "category": "Tools",
    "depends": ["base", "account", "mail", "website"],
    "license": "LGPL-3",
    "data": [
        "security/ir.model.access.csv",
        "views/brand_views.xml",
        "views/phone_views.xml",
        "views/tags.xml",
        "views/phone_call_views.xml",
        # "views/phone_store_stage_data.xml",
        "views/website_snippets.xml",  # Make sure this is included
    ],
    "assets": {
        "web.assets_frontend": [
            "phone_store/static/src/js/phone_snippet.js",
        ],
    },
    "installable": True,
    "application": True,
}

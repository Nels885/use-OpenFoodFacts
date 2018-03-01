"""
Variables Globales
"""


class Glob:

    confDbFile = 'data/database_conf'

    infoApi = {
        'https': 'https://fr.openfoodfacts.org/cgi/search.pl?search_simple=1&action=process',
        'action': 'process',
        'sort_by': 'unique_scans_n',
        'page_size': '20',
        'json': '1',
        'tagtype_0': 'countries',
        'tag_contains_0': 'contains',
        'tag_0': 'france',
        'tagtype_1': 'categories',
        'tag_contains_1': 'contains'
    }

    categories = [
        'Boissons gazeuses', 'Boissons chaudes', 'Boissons non sucrées', 'Laits', 'Yaourts', 'Fromages',
        'Plats préparés', 'Céréales et pommes de terre', 'Biscuits et gateaux', 'Desserts', 'Confiseries',
        'Légumes et dérivées'
    ]

    converDb = {
        'product': {
            'product_name': 'product_name',
            'quantite': 'qauntity',
            'ingredient': 'ingredients_text_with_allergens_fr',
            'nutrition_grade': 'nutrition_grades',
            'url': 'url',
            'stores': 'stores_tags'
        },
        'categorie': {
            'name': 'categories_tags'
        }
    }

"""
Variables Globales
"""


class Glob:

    infoApi = {
        'https': 'https://fr.openfoodfacts.org/cgi/search.pl?search_simple=1&action=process',
        'action': 'process',
        'tagtype_0': 'countries',
        'tag_contains_0': 'contains',
        'tag_0': 'france',
        'sort_by': 'unique_scans_n',
        'page_size': '20',
        'json': '1'
    }

    categories = [
        'Boissons gazeuses', 'Boissons chaudes', 'Boissons non sucrées', 'Laits', 'Yaourts', 'Fromages',
        'Plats préparés', 'Céréales et pommes de terre', 'Biscuits et gateaux', 'Desserts', 'Confiseries',
        'Légumes et dérivées'
    ]

    converDb = {
        'categories_tags': ['categorie', 'name'],
        'product_name': ['product', 'product_name'],
        'ingredients_text_with_allergens_fr': ['product', 'ingredient'],
        'url': ['product', 'url'],
        'nutrition_grades': ['product', 'nutrition_grade'],
        'stores_tags': ['store', 'name']
    }

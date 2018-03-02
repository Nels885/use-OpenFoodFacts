"""
Global variables module
"""


class Glob:
    """
    List of variables used by different Python script
    """

    # Path for the configuration file
    confDbFile = 'data/database_conf'

    # Constants for SQL requests
    reqSelect = """SELECT %s FROM %s;"""
    reqCondition = """SELECT %s FROM %s WHERE %s %s;"""
    tabAssocCat = "product AS p, assoc_product_categorie AS a, categorie AS c"
    condAssocCat = "p.id=a.product_id AND c.id=a.categorie_id"

    # Information for the OpenFoodFacts API
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

    # List of categories for the database
    categories = [
        'Boissons gazeuses', 'Boissons chaudes', 'Boissons non sucrées', 'Laits', 'Yaourts', 'Fromages',
        'Plats préparés', 'Céréales et pommes de terre', 'Biscuits et gateaux', 'Desserts', 'Confiseries',
        'Légumes et dérivés'
    ]

    # Not used
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

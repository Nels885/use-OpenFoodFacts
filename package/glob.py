"""
Global variables module
"""


class Glob:
    """
    List of variables used by different Python script
    """

    # Path for the configuration file
    confDbFile = 'database_conf'

    # Constants for SQL requests
    tabAssocCat = "product AS p, assoc_product_categorie AS a, categorie AS c"
    condAssocCat = "p.id=a.product_id AND c.id=a.categorie_id"
    tabBackProd = "backup AS b, product AS p"
    condBackProd = "b.product_id=p.id"

    # Information for the OpenFoodFacts API
    infoApi = {
        'https': 'https://fr.openfoodfacts.org/cgi/search.pl?search_simple=1&action=process',
        'action': 'process',
        'sort_by': 'unique_scans_n',
        'page_size': '100',
        'json': '1',
        'tagtype_0': 'countries',
        'tag_contains_0': 'contains',
        'tag_0': 'france',
        'tagtype_1': 'categories',
        'tag_contains_1': 'contains'
    }

    # Parameters for inserting data into the database
    converDb = {
        'product': [
            ('product_name', 'product_name'),
            ('quantite', 'quantity'),
            ('ingredient', 'ingredients_text_with_allergens_fr'),
            ('nutrition_grade', 'nutrition_grades'),
            ('url', 'url'),
            ('stores', 'stores_tags')
        ],
        'categorie': (
            'Boissons gazeuses', 'Boissons chaudes', 'Boissons non sucrées', 'Laits', 'Yaourts', 'Fromages',
            'Plats préparés', 'Céréales et pommes de terre', 'Biscuits et gateaux', 'Desserts', 'Confiseries',
            'Légumes et dérivés'
        ),
        'assoc_product_categorie': (
            'product_id',
            'categorie_id'
        ),
        'backup': (
            'id',
            'product'
        )
    }

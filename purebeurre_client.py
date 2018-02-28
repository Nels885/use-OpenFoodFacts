#! /usr/bin/env python3
# coding: utf-8

import pickle
import logging as log

from data.sql import Sql


def list_categories():
    categories = db.sql_select("""SELECT * FROM categorie;""")
    while 1:
        print("\nListes des catégories:")
        number = []
        for cat in categories:
            number.append(str(cat[0]))
            print(" {} - {}".format(cat[0], cat[1]))
        categorieId = input("Entrez le numéro de votre choix ( ou <Enter> pour quitter) : ")
        if categorieId in number:
            break
    return categorieId


def list_products(categorieId):
    searchProduct = """
                    SELECT
                          p.id,
                          p.product_name,
                          p.nutrition_grade,
                          c.name
                    FROM
                          product AS p,
                          assoc_product_categorie AS a,
                          categorie AS c
                    WHERE
                          p.id=a.product_id AND c.id=a.categorie_id AND c.id='%s';
                    """
    products = db.sql_select(searchProduct % categorieId)
    while 1:
        print("\nListes des produits:")
        number = []
        for prod in products:
            number.append(str(prod[0]))
            print(" {} - {}".format(prod[0], prod[1]))
        productId = input("Entrez le numéro de votre choix ( ou <Enter> pour quitter) : ")
        if productId in number:
            break
    return products[int(productId)]


def surrogate_products(product):
    surrogateProduct = """
                        SELECT
                            p.product_name,
                            p.ingredient,
                            p.url,
                            p.stores
                        FROM
                            product AS p,
                            assoc_product_categorie AS a,
                            categorie AS c
                        WHERE
                            p.id=a.product_id AND c.id=a.categorie_id AND c.name='%s' AND p.nutrition_grade='%s';
                        """
    surrogate = db.sql_select(surrogateProduct % (product[3], product[2]))
    for info in surrogate:
        print(info)


def list_backup():
    pass


def main():
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
          "~~       Recherche de produit          ~~\n"
          "~~            Pure Beurre              ~~\n"
          "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    print("\nListes des options:\n"
          " 1 - Quel aliment souhaitez-vous remplacer ?\n"
          " 2 - retrouvez mes aliments substitués\n")
    entry = input("Entrez le numéro de votre choix ( ou <Enter> pour quitter) : ")
    return entry


if __name__ == '__main__':
    log.basicConfig(level=log.INFO)
    try:
        confDatabase = pickle.load(open('database_conf', 'rb'))
        while 1:
            choice = main()
            db = Sql(log, confDatabase)
            if choice == "":
                break
            elif choice == "1":
                surrogate_products(list_products(list_categories()))
            elif choice == "2":
                list_backup()
            db.sql_close()
    except KeyboardInterrupt:
        log.warning("Fermeture du programme avec Ctrl+C")
        db.sql_close()
    except FileNotFoundError:
        log.error("Manque fichier 'database_conf' voyez lancer le script 'update_db.py'")

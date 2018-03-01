#! /usr/bin/env python3
# coding: utf-8
"""

"""
import os
import pickle
import logging as log

from random import randint

from data.database import Database


def list_categories():
    categories = db.select("""SELECT * FROM categorie;""")
    while 1:
        print("\nListes des catégories:")
        nb = 0
        numbers = []
        for cat in categories:
            nb += 1
            numbers.append(str(nb))
            print(" {} - {}".format(len(numbers), cat[1]))
        categorieId = input("Entrez le numéro de votre choix : ")
        if categorieId in numbers:
            break
    return categories[int(categorieId) - 1]


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
    products = db.select(searchProduct % categorieId[0])
    while 1:
        print("\nListes des produits:")
        nb = 0
        numbers = []
        for prod in products:
            nb += 1
            numbers.append(str(nb))
            print(" {} - {}".format(nb, prod[1]))
        productId = input("Entrez le numéro de votre choix : ")
        if productId in numbers:
            break
    return products[int(productId) - 1]


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
    surrogate = db.select(surrogateProduct % (product[3], product[2]))
    nb = randint(0, len(surrogate) - 1)
    os.system("clear")
    print(
        "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n"
        " Proposition de produit de substitution pour '{}':\n"
        "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n"
        " * Nom : {}\n"
        " * Ingredients : {}\n"
        " * URL OpenFoodfacts : {}\n"
        " * Magasins : {}\n"
        .format(product[1], surrogate[nb][0], surrogate[nb][1], surrogate[nb][2], surrogate[nb][3])
    )
    input("Appuyez sur une touche pour revenir au menu principal... ")


def list_backup():
    pass


def main():
    os.system("clear")
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
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
            db = Database(log, confDatabase)
            if choice == "":
                break
            elif choice == "1":
                surrogate_products(list_products(list_categories()))
            elif choice == "2":
                list_backup()
            db.close()
    except KeyboardInterrupt:
        log.warning("Fermeture du programme avec Ctrl+C")
        db.close()
    except FileNotFoundError:
        log.error("Manque fichier 'database_conf' voyez lancer le script 'update_db.py'")

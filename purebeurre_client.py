#! /usr/bin/env python3
# coding: utf-8
"""

"""
import os
import pickle
import logging as log
import argparse

from random import randint

from data.database import Database
from data.glob import Glob


def list_categories():
    categories = db.select("""SELECT * FROM categorie;""")
    while 1:
        os.system("clear")
        print("\nListes des catégories:")
        nb = 0
        numbers = []
        for cat in categories:
            nb += 1
            numbers.append(str(nb))
            print(" {} - {}".format(len(numbers), cat[1]))
        selectId = input("Entrez le numéro de votre choix : ")
        if selectId in numbers:
            break
    return categories[int(selectId) - 1]


def parse_arguments():
    """
    Arguments added to command line to get
    additional information
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action='store_true', help="""Display informations of use-OpenFoodFacts""")
    parser.add_argument("-d", "--debug", action='store_true', help="""Switch to debug mode!""")
    return parser.parse_args()


def list_products(infoCategorie):
    catId, catName = infoCategorie
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
    products = db.select(searchProduct % catId)
    while 1:
        os.system("clear")
        print("\nListes des produits de la Catégorie '{}' :".format(catName))
        nb = 0
        numbers = []
        for prod in products:
            nb += 1
            numbers.append(str(nb))
            print(" {} - {}".format(nb, prod[1]))
        selectId = input("Entrez le numéro de votre choix : ")
        if selectId in numbers:
            break
    return products[int(selectId) - 1]


def surrogate_products(product):
    prodId, prodName, prodGrade, catName = product
    surrogateProduct = """
                        SELECT
                            p.product_name,
                            p.quantite,
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
    surrogate = db.select(surrogateProduct % (catName, prodGrade))
    nb = randint(0, len(surrogate) - 1)
    name, quantity, ingredients, url, stores = surrogate[nb]
    os.system("clear")
    print(
        "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n"
        " Proposition produit de substitution pour '{}':\n"
        "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n"
        " * Nom : {}\n"
        " * Quantité : {}\n"
        " * Ingredients : {}\n"
        " * URL OpenFoodfacts : {}\n"
        " * Magasins : {}\n"
        .format(prodName, name, quantity, ingredients, url, stores)
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
    args = parse_arguments()
    if args.debug:
        log.basicConfig(level=log.DEBUG)
    elif args.verbose:
        log.basicConfig(level=log.INFO)
    try:
        confDatabase = pickle.load(open(Glob.confDbFile, 'rb'))
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

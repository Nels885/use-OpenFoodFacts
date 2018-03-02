#! /usr/bin/env python3
# coding: utf-8
"""
'Pure Beurre' Software for product substitution research
"""

import os
import pickle
import logging as log
import argparse

from random import randint

from data.database import Database
from data.glob import Glob


def parse_arguments():
    """
    Arguments added to command line to get
    additional information
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action='store_true',
                             help="""Display informations of use-OpenFoodFacts""")
    parser.add_argument("-d", "--debug", action='store_true', help="""Switch to debug mode!""")
    return parser.parse_args()


def header():
    """
    Header of the programm in the console
    """
    os.system("clear")
    print("\n   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
          "   ~~~               Programme Pure Beurre             ~~~\n"
          "   ~~~        Recherche produit de substitution        ~~~\n"
          "   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


def list_categories():
    """
    List categories in the console and ask
    the user for input a number.
        :return: returns the number that the user has chosen
    """
    cols = "*"
    tabCat = "categorie"
    categories = db.select(cols, tabCat)
    while 1:
        header()
        print("\nListes des catégories:")
        nb = 0
        numbers = []
        for cat in categories:
            nb += 1
            numbers.append(str(nb))
            print("  {} - {}".format(len(numbers), cat[1]))
        selectId = input("Entrez le numéro de votre choix : ")
        if selectId in numbers:
            break
    return categories[int(selectId) - 1]


def list_products(infoCategory):
    """
    List the products of the chosen category and ask
    the user for input a number.
        :param infoCategory: Id of the category
        :return: returns the number that the user has chosen
    """
    catId, catName = infoCategory
    cols = "p.id,p.product_name,p.nutrition_grade,c.name"
    searchProduct = " AND c.id=%s"
    condition = Glob.condAssocCat + searchProduct
    values = [catId]
    products = db.select(cols, Glob.tabAssocCat, condition, values, True)
    while 1:
        header()
        print("\nListes des produits de la Catégorie '{}' :".format(catName))
        nb = 0
        numbers = []
        for prod in products:
            nb += 1
            numbers.append(str(nb))
            print("  {} - {}".format(nb, prod[1]))
        selectId = input("Entrez le numéro de votre choix : ")
        if selectId in numbers:
            break
    return products[int(selectId) - 1]


def surrogate_products(product):
    """
    Displays the description of the substitution
    product selected by the user
        :param product: tuple grouping the product information
        :return: Displays in the console the product information
    """
    prodId, prodName, prodGrade, catName = product
    cols = "p.product_name,p.quantite,p.ingredient,p.url,p.stores"
    surrogateCondition = " AND c.name=%s AND p.nutrition_grade=%s"
    condition = Glob.condAssocCat + surrogateCondition
    values = [catName, prodGrade]
    surrogate = db.select(cols, Glob.tabAssocCat, condition, values, True)
    nb = randint(0, len(surrogate) - 1)
    name, quantity, ingredients, url, stores = surrogate[nb]
    os.system("clear")
    print(
        "\n##########################################################################\n\n"
        "  Proposition produit de substitution pour '{}':\n"
        "\n##########################################################################\n\n"
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
    """
    Principal menu of the program
        :return: returns the number that the user has chosen
    """
    print("\nListes des options:\n"
          "  1 - Quel aliment souhaitez-vous remplacer ?\n"
          "  2 - retrouvez mes aliments substitués\n")
    entry = input("Entrez le numéro de votre choix ( ou <Enter> pour quitter) : ")
    return entry


if __name__ == '__main__':
    """
    Initialization of program
    """
    args = parse_arguments()
    if args.debug:
        log.basicConfig(level=log.DEBUG)
    elif args.verbose:
        log.basicConfig(level=log.INFO)
    try:
        confDatabase = pickle.load(open(Glob.confDbFile, 'rb'))
        while 1:
            header()
            db = Database(log, confDatabase)
            if not db.error:
                choice = main()
                if choice == "":
                    break
                elif choice == "1":
                    surrogate_products(list_products(list_categories()))
                elif choice == "2":
                    list_backup()
                db.close()
            else:
                print("\n*** Erreur information de connection base de données ***\n")
                break
    except KeyboardInterrupt:
        log.warning("Fermeture du programme avec Ctrl+C")
    except FileNotFoundError:
        log.error("Manque fichier 'database_conf' voyez lancer le script 'update_db.py'")
    else:
        db.close()

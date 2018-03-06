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
    condition = Glob.condAssocCat + " AND c.id=%s"
    values = [catId]
    products = db.select(cols, Glob.tabAssocCat, condition, True, values)
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
    cols = "p.id,p.product_name,p.quantite,p.ingredient,p.url,p.stores"
    condition = Glob.condAssocCat + " AND c.name=%s AND p.nutrition_grade=%s"
    values = [catName, prodGrade]
    surrogate = db.select(cols, Glob.tabAssocCat, condition, True, values)
    nb = randint(0, len(surrogate) - 1)
    subBackup = [surrogate[nb][0], prodName]
    while 1:
        desc_product(surrogate[nb][1:], prodName)
        print("Listes des options:\n"
              "  1 - Enregistrez cet aliment de substitution ?\n"
              "  2 - Pour retournez au menu principale\n")
        entry = input("Entrez le numéro de votre choix : ")
        if entry == "1":
            list_backup(subBackup)
            break
        elif entry == "2":
            break


def desc_product(infoSub, subName):
    name, quantity, ingredients, url, stores = infoSub
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
        .format(subName, name, quantity, ingredients, url, stores)
    )


def list_backup(subBackup=None):
    if subBackup is None:
        cols = "b.id,b.substituted_product,p.id,p.product_name,p.quantite,p.ingredient,p.url,p.stores"
        condition = Glob.condBackProd
        backups = db.select(cols, Glob.tabBackProd, condition, True)
        while 1:
            header()
            numbers = []
            print("\nListes des produits substitués :")
            for back in backups:
                numbers.append(str(back[0]))
                print("  {} - '{}' substitut de : '{}'".format(back[0], back[3], back[1]))
            selectId = input("\nEntrez le numéro de votre choix ou <Enter> pour le menu principal : ")
            if selectId == "":
                break
            elif selectId in numbers:
                backup = backups[int(selectId) - 1]
                print(backup)
                desc_product(backup[3:], backup[1])
                input("Appuyez sur une touche pour revenir au menu principal... ")
                break
    else:
        log.info("Info backup : %s", subBackup)
        db.insert("backup", subBackup, "product_id,substituted_product")
        print("\n## Enregistrement du produit de substitution termné ##\n")
        input("Appuyez sur une touche pour revenir au menu principal... ")


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

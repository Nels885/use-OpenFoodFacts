#! /usr/bin/env python3
# coding: utf-8
"""
'Pure Beurre' Software for product substitution research
"""

import os
import pickle
import logging as log
import argparse

from package.database import Database
from package.glob import Glob


def parse_arguments():
    """
    Arguments added to command line to get
    additional information
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action='store_true', help="""Display informations of use-OpenFoodFacts""")
    parser.add_argument("-d", "--debug", action='store_true', help="""Switch to debug mode!""")
    return parser.parse_args()


def header():
    """
    Header of the program in the console
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

    # list of categories of the category table
    cols = "*"
    tabCat = "category ORDER BY name"
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
    values = [catId]

    # list of products of the selected category using the association table "assoc_product_category"
    cols = "p.id,p.product_name,p.nutrition_grade,c.name"
    condition = Glob.condAssocCat + " AND c.id=%s ORDER BY p.product_name"
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


def substitute_products(product):
    """
    Displays the description of the substitution
    product selected by the user
        :param product: tuple grouping the product information
        :return: Displays in the console the product information
    """
    prodId, prodName, prodGrade, catName = product
    values = [catName, prodGrade]

    # list of substitute products
    cols = "p.id,p.product_name,p.quantity,p.ingredient,p.url,p.stores"
    condition = Glob.condAssocCat + " AND c.name=%s AND p.nutrition_grade=%s"
    subProducts = db.select(cols, Glob.tabAssocCat, condition, True, values)

    nb = 0
    while 1:
        desc_product(subProducts[nb][1:], prodName)
        print("Listes des options:\n"
              "  1 - Produit de substitution suivant...\n"
              "  2 - Enregistrez cet aliment de substitution ?\n"
              "  3 - Pour retournez au menu principale\n")
        entry = input("Entrez le numéro de votre choix : ")
        if entry == "1":
            if nb < (len(subProducts) - 1):
                nb += 1
            else:
                input("\nAppuyez sur une touche pour revenir au premier produit de substitution... ")
                nb = 0
        if entry == "2":
            subBackup = [subProducts[nb][0], prodName]
            list_backup(subBackup)
            break
        elif entry == "3":
            break


def desc_product(infoSub, subName):
    """
    Display different values of a product
        :param infoSub: Tuple of substitute product values
        :param subName: Name of the substituted product
    """
    name, quantity, ingredients, url, stores = infoSub
    os.system("clear")
    print(
        "\n   ##########################################################################\n\n"
        "     Proposition produit de substitution pour '{}':\n"
        "\n   ##########################################################################\n\n"
        " * Nom : {}\n"
        " * Quantité : {}\n"
        " * Ingredients : {}\n"
        " * URL OpenFoodfacts : {}\n"
        " * Magasins : {}\n".format(subName, name, quantity, ingredients, url, stores))


def list_backup(subBackup=None):
    """
    Displays the list of registered substitute products
        :param subBackup: Tuple of the list substitute products of the backup table
        :return: Displays in the console the list
    """
    if subBackup is None:
        cols = "b.id,b.substituted_product,p.id,p.product_name,p.quantity,p.ingredient,p.url,p.stores"
        condition = Glob.condBackProd
        backups = db.select(cols, Glob.tabBackProd, condition, True)
        while 1:
            header()
            nb = 0
            numbers = []
            print("\nListes des produits substitués :")
            for back in backups:
                backId, subProd, prodId, ProdName = back[:4]
                nb += 1
                numbers.append(str(nb))
                print("  {} - '{}' substitut de : '{}'".format(nb, ProdName, subProd))
            selectId = input("\nEntrez le numéro de votre choix ou <Enter> pour le menu principal : ")
            if selectId == "":
                break
            elif selectId in numbers:
                backup = backups[int(selectId) - 1]
                desc_product(backup[3:], backup[1])
                input("Appuyez sur une touche pour revenir au menu principal... ")
                break
    else:
        log.info("Info backup : %s", subBackup)
        db.insert("backup", subBackup, "product_id,substituted_product")
        print("\n## Enregistrement du produit de substitution terminé ##\n")
        input("Appuyez sur une touche pour revenir au menu principal... ")


def del_backup():
    """
    Displays the list of registered substitute products to be erased
    """
    cols = "b.id,b.substituted_product,p.id,p.product_name,p.quantity,p.ingredient,p.url,p.stores"
    condition = Glob.condBackProd
    backups = db.select(cols, Glob.tabBackProd, condition, True)
    while 1:
        header()
        numbers = []
        print("\nListes des produits substitués :")
        for back in backups:
            backId, subProd, prodId, ProdName = back[:4]
            numbers.append(str(backId))
            print("  {} - '{}' substitut de : '{}'".format(backId, subProd, ProdName))
        print("\nListes des options:\n"
              "  - Choisir le numéro du produit à retirer\n"
              "  - Taper 'all' pour retirer tout les produits\n"
              "  - La touche <Enter> pour le menu principal\n")
        selectId = input("Entrez votre choix : ")
        if selectId == "":
            break
        else:
            if selectId in numbers:
                cmd = "DELETE FROM backup WHERE id=%s;"
                db.execute(cmd, [selectId])
                print("\n## Le produit N°%s a été retiré ##\n" % selectId)
            elif selectId == "all":
                cmd = "DELETE FROM backup; SELECT setval('backup_id_seq',1, false);"
                db.execute(cmd)
                print("\n## Tout les produits enregistrés sont retirés de la base ##\n")
            input("Appuyez sur une touche pour revenir au menu principal... ")
            break


def main():
    """
    Principal menu of the program
        :return: returns the number that the user has chosen
    """
    print("\nListes des options:\n"
          "  1 - Quel aliment souhaitez-vous remplacer ?\n"
          "  2 - Retrouvez mes aliments substitués\n"
          "  3 - Supprimez mes aliments substitués\n")
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
                    substitute_products(list_products(list_categories()))
                elif choice == "2":
                    list_backup()
                elif choice == "3":
                    del_backup()
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

#! /usr/bin/env python3
# coding: utf-8
"""
Update database PostgreSQL with API OpenfoodFacts
"""

import os
import pickle
import logging as log
from getpass import getpass
import argparse

from data.database import Database
from data.glob import Glob
from data.apirest import Apirest


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


def header(msg="\n"):
    os.system("clear")
    print("\n   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
          "   ~~~           Mise à jour Base de données           ~~~\n"
          "   ~~~         pour l'application  Pure Beurre         ~~~\n"
          "   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(msg)


def conf_database(msg="\n"):
    """
    Adding the parameters in the 'database_conf' file that
    allow you to connect to the database
        :return: dict of the parameters of the database
    """
    while True:
        header(msg)
        print("Information de connection pour la base de données")
        dbname = input("  - Nom de la base de données : ")
        user = input("  - Compte propriétaire : ")
        password = getpass("  - Password du compte : ")
        port = str(input("  - port (5432 par défaut) : "))
        if port == "":
            port = "5432"
        host = input("  - Adresse base de données ('localhost' par défaut) : ")
        if host == "":
            host = "localhost"
        confDb = {'dbname': dbname, 'user': user, 'password': password, 'port': port, 'host': host}
        pickle.dump(confDb, open(Glob.confDbFile, 'wb'))
        testDb = Database(log, confDb)
        if not testDb.error:
            break
        else:
            print("\n*** Erreur information de connection base de données ***\n")
            input("Appuyez sur une touche pour modifier les paramètres... ")

    print("\n## Ajout paramètres de la base de données terminée ##\n")


def data_create():
    """
    Adding data from OpenFoodFacts to the database using
    the OpenFoodFacts API and using SQL requests
        :return: Adding values in the different tables of the database
    """
    api = Apirest(log)
    info = ['product_name', 'ingredients_text_with_allergens_fr', 'quantity', 'nutrition_grades', 'url']

    for categorie in Glob.categories:
        result = api.get_request(categorie)
        insertCategorie = """INSERT INTO categorie(name) VALUES('%s') RETURNING id;"""
        idCategorie = db.insert_id(insertCategorie % categorie)
        for number in range(len(result) - 1):
            val = []
            log.info("*** PRODUIT N°%s CATEGORIE : '%s' ***\n", str(number + 1), categorie)
            log.info("** Product_name : %s", result[number]['product_name'])
            for nb in range(len(info)):
                try:
                    case = result[number][info[nb]].strip()
                    repVal = {"'": " ", '<span class="allergen">': '', '</span>': '', '\r': ' '}
                    for key, value in repVal.items():
                        case = case.replace(key, value)
                    val.append(case)
                except KeyError as err:
                    val.append("NULL")
                    log.warning("*** Valeur absente: %s", err)
                except AttributeError:
                    val.append("NULL")
            stores = ", ".join(result[number]['stores_tags'])
            valProduct = (val[0], val[1], val[2], val[3], val[4], stores)
            colProduct = "product_name,ingredient,quantite,nutrition_grade,url,stores"
            log.info("%s\n", valProduct)
            tableProduct = "product"
            insertProduct = """INSERT INTO {}({}) VALUES('%s','%s','%s','%s','%s','%s') RETURNING id;""".format(tableProduct,colProduct)
            idProduct = db.insert_id(insertProduct % valProduct)
            db.execute("""INSERT INTO assoc_product_categorie VALUES('%s','%s');""" % (idProduct, idCategorie))
    print("\n## Insertion des données dans la base terminée ##\n")


def main():
    """
    Principal menu of the program
        :return: returns the number that the user has chosen
    """
    header()
    print("Listes des options:\n"
          "  1 - Paramètres base de données\n"
          "  2 - Creation base de données\n"
          "  3 - Effacez la base de données\n"
          "  4 - Insérez données dans la base de données\n")
    entry = input("Entrez le numéro de votre choix (ou <Enter> pour quitter) : ")
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
    while 1:
        try:
            confDb = pickle.load(open(Glob.confDbFile, 'rb'))
            db = Database(log, confDb)
            choice = main()
            if choice == "":
                break
            if not db.error:
                if choice == "1":
                    conf_database()
                elif choice == "2":
                    header("\n## Creation de la base de données ##\n")
                    db.sql_script('script_create_DB.sql')
                elif choice == "3":
                    header("\n## Suppression des données dans la base ##\n")
                    db.sql_script('script_erase_DB.sql')
                elif choice == "4":
                    header("\n## Insertion des données dans la base en cours... ##\n")
                    data_create()
                else:
                    print("\n*** Erreur de touche ***\n")
            else:
                conf_database("\n*** Erreur information de connection Base de données ***\n")
            input("Appuyez sur une touche pour revenir au menu principal... ")
            db.close()
        except FileNotFoundError:
            conf_database()
            continue
        except KeyboardInterrupt:
            log.warning("Fermeture du programme avec Ctrl+C")
            break
        else:
            db.close()


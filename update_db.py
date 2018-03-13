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

from package.database import Database
from package.glob import Glob
from package.apirest import Apirest


def parse_arguments():
    """
    Arguments added to command line to get
    additional information
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action='store_true', help="""Display informations of use-OpenFoodFacts""")
    parser.add_argument("-d", "--debug", action='store_true', help="""Switch to debug mode!""")
    return parser.parse_args()


def header(msg=""):
    """
    Header of program
        :param msg: Show the menu name or detected errors
        :return: Show the program header
    """
    os.system("clear")
    print("\n   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
          "   ~~~           Mise à jour Base de données           ~~~\n"
          "   ~~~         pour l'application Pure Beurre          ~~~\n"
          "   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
    print(msg)


def conf_database(msg=""):
    """
    Adding the parameters in the 'database_conf' file that
    allow you to connect to the database
        :return: dict of the parameters of the database
    """
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
    confDatabase = {'dbname': dbname, 'user': user, 'password': password, 'port': port, 'host': host}
    pickle.dump(confDatabase, open(Glob.confDbFile, 'wb'))

    print("\n## Ajout paramètres de la base de données terminée ##\n")


def data_create():
    """
    Adding data from OpenFoodFacts to the database using
    the OpenFoodFacts API and using SQL requests
        :return: Adding values in the different tables of the database
    """
    api = Apirest(log)
    col = []
    dataOffName = []
    tableProd = "product"
    tableCat = "categorie"
    for colDb, name in Glob.converDb[tableProd]:
        if name is not None:
            dataOffName.append(name)
        col.append(colDb)
    colProduct = ",".join(col)
    log.info("Colonnes : %s\n"
             "Valeurs  : %s" % (colProduct, dataOffName))

    nbLineBefore = db.select("count(*)", tableProd)[0][0]

    for categorie in Glob.converDb[tableCat]:
        condCat = " name=%s"
        catId = db.select("id", tableCat, condCat, True, [categorie])
        if len(catId) == 0:
            idCategorie = db.insert(tableCat, [categorie], "name", True)
        else:
            idCategorie = catId[0][0]
            log.info("*** Categorie '%s' existe avec l'ID : %s ***" % (categorie, idCategorie))
        results = api.get_request(categorie)
        for nbProduct in range(len(results) - 1):
            result = results[nbProduct]
            valProduct = api.convert_data(result, dataOffName)

            # Product information with verbose option
            log.info("*** PRODUIT N°%s CATEGORIE : '%s' ***\n"
                     "Product_name : %s\n", str(nbProduct + 1), categorie, result['product_name'])
            log.debug("Valeurs du produit : %s\n", valProduct)

            condition = " product_name=%s"
            listId = db.select("id", tableProd, condition, True, [result['product_name']])
            if len(listId) == 0:
                idProduct = db.insert(tableProd, valProduct, colProduct, True)
            else:
                idProduct = listId[0][0]
                log.info("*** Produit '%s' existe avec l'ID : %s ***" % (result['product_name'], idProduct))
            db.insert("assoc_product_categorie", [idProduct, idCategorie])

    nbLineAfter = db.select("count(*)", tableProd)[0][0]
    print("  - {} produits ajoutés\n"
          "\n## Insertion des données dans la base terminée ##\n".format(nbLineAfter - nbLineBefore))


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
            if not db.error:
                choice = main()
                if choice == "":
                    break
                elif choice == "1":
                    conf_database()
                elif choice == "2":
                    header("## Creation de la base de données ##\n")
                    db.sql_script('script_create_DB.sql')
                elif choice == "3":
                    header("## Suppression des données dans la base ##\n")
                    db.sql_script('script_erase_DB.sql')
                elif choice == "4":
                    header("# Insertion des données dans la base en cours... #\n")
                    data_create()
                else:
                    print("\n*** Erreur de touche ***\n")
            else:
                conf_database("*** Erreur information de connection Base de données ***\n")
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

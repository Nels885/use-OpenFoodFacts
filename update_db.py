#! /usr/bin/env python3
# coding: utf-8
"""
Update database PostgreSQL with API OpenfoodFacts
"""

import requests
import pickle
import logging as log
from getpass import getpass

from data.database import Database
from data.glob import Glob


def conf_database():
    print("\nInformation de connection pour la base de données")
    dbname = input("- Nom de la base de données : ")
    user = input("- Compte propriétaire : ")
    password = getpass("- Password du compte : ")
    port = str(input("- port (5432 par défaut) : "))
    if port == "":
        port = "5432"
    host = input("- Adresse base de données ('localhost' par défaut) : ")
    if host == "":
        host = "localhost"
    confDb = {'dbname': dbname, 'user': user, 'password': password, 'port': port, 'host': host}
    pickle.dump(confDb, open('database_conf', 'wb'))
    return confDb


def data_create():
    cmdRequest = "{}&action={}&tagtype_0={}&tag_contains_0={}&tag_0={}&sort_by={}&page_size={}&json={}".format(
        Glob.infoApi['https'],
        Glob.infoApi['action'],
        Glob.infoApi['tagtype_0'],
        Glob.infoApi['tag_contains_0'],
        Glob.infoApi['tag_0'],
        Glob.infoApi['sort_by'],
        Glob.infoApi['page_size'],
        Glob.infoApi['json'])

    info = ['product_name', 'ingredients_text_with_allergens_fr', 'quantity', 'nutrition_grades', 'url']

    for categorie in Glob.categories:
        r = requests.get("{}&tagtype_1=categories&tag_contains_1=contains&tag_1={}".format(cmdRequest, categorie))
        print("# Status Code: {} #".format(r.status_code))
        print("# Headers: {} #".format(r.headers['content-type']))
        print()
        result = r.json()['products']
        insertCategorie = """INSERT INTO categorie(name) VALUES('%s') RETURNING id;"""
        idCategorie = db.insert_id(insertCategorie % categorie)
        for number in range(len(result) - 1):
            val = []
            log.info("*** PRODUIT N°%s CATEGORIE : '%s' ***\n", str(number + 1), categorie)
            log.info("** Product_name : %s", result[number]['product_name'])
            for nb in range(len(info)):
                try:
                    case = result[number][info[nb]].strip()
                    repVal = {"'": " ", '<span class="allergen">': '', '</span>': '', '\n': ' '}
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

            # for sto in result[number]['stores_tags']:
            #     insertStore = """INSERT INTO store(name) VALUES('%s') ON CONFLICT (name) DO NOTHING;""" % sto
            #     db.sql_request(insertStore)
            # for cat in result[number]['categories_tags']:
            #     insertCategorie = """INSERT INTO categorie(name) VALUES('%s') ON CONFLICT (name) DO NOTHING;""" % cat
            #     db.sql_request(insertCategorie)
            #     # db.sql_insert("categorie", "name", cat)


def main():
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
          "~~     Mise à jour Base de données     ~~\n"
          "~~            Pure Beurre              ~~\n"
          "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    try:
        confDatabase = pickle.load(open('database_conf', 'rb'))
    except FileNotFoundError:
        confDatabase = conf_database()
    print("\nListes des options:\n"
          " 1 - Paramètres base de données\n"
          " 2 - Creation base de données\n"
          " 3 - Effacez la base de données\n"
          " 4 - Insérez données dans la base de données\n")
    entry = input("Entrez le numéro de votre choix ( ou <Enter> pour quitter) : ")
    return entry, confDatabase


if __name__ == '__main__':
    log.basicConfig(level=log.INFO)
    try:
        while 1:
            choice, confSql = main()
            db = Database(log, confSql)
            if choice == "":
                break
            elif choice == "1":
                confSql = conf_database()
            elif choice == "2":
                db.sql_script('script_create_DB.sql')
            elif choice == "3":
                db.sql_script('script_erase_DB.sql')
            elif choice == "4":
                data_create()
            db.close()
    except KeyboardInterrupt:
        log.warning("Fermeture du programme avec Ctrl+C")
        db.close()

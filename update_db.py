#! /usr/bin/env python3
# coding: utf-8

import requests
import pickle
import logging as log
from getpass import getpass

from data.sql import Sql

converDb = {
    'categories_tags': ['categorie', 'name'],
    'product_name': ['product', 'product_name'],
    'ingredients_text_with_allergens_fr': ['product', 'ingredient'],
    'url': ['product', 'url'],
    'nutrition_grades': ['product', 'nutrition_grade'],
    'stores_tags': ['store', 'name']
}

infoRequest = {
    'https': 'https://fr.openfoodfacts.org/cgi/search.pl?search_simple=1&action=process',
    'action': 'process',
    'tagtype_0': 'countries',
    'tag_contains_0': 'contains',
    'tag_0': 'france',
    'sort_by': 'unique_scans_n',
    'page_size': '20',
    'json': '1'
}

categories = [
    'Boissons gazeuses', 'Boissons chaudes', 'Boissons non sucrées', 'Laits', 'Yaourts', 'Fromages',
    'Plats préparés', 'Céréales et pommes de terre', 'Biscuits et gateaux', 'Desserts', 'Confiseries',
    'Légumes et dérivées'
]


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
        infoRequest['https'],
        infoRequest['action'],
        infoRequest['tagtype_0'],
        infoRequest['tag_contains_0'],
        infoRequest['tag_0'],
        infoRequest['sort_by'],
        infoRequest['page_size'],
        infoRequest['json'])

    info = ['product_name', 'ingredients_text_with_allergens_fr', 'quantity', 'nutrition_grades', 'url']

    for categorie in categories:
        r = requests.get("{}&tagtype_1=categories&tag_contains_1=contains&tag_1={}".format(cmdRequest, categorie))
        print("# Status Code: {} #".format(r.status_code))
        print("# Headers: {} #".format(r.headers['content-type']))
        print()
        result = r.json()['products']
        insertCategorie = """INSERT INTO categorie(name) VALUES('%s') RETURNING id;""" % categorie
        idCategorie = db.sql_insert_id(insertCategorie)
        for number in range(len(result) - 1):
            val = []
            print("\n*** PRODUIT N°{} ***\n".format(str(number + 1)))
            print(result[number]['product_name'])
            for nb in range(len(info)):
                try:
                    val.append(result[number][info[nb]].replace("'", " "))
                except KeyError as err:
                    val.append("NULL")
                    print("*** Valeur absente: {}".format(err))
                except AttributeError:
                    val.append("NULL")
            stores = ", ".join(result[number]['stores_tags'])
            values = (val[0], val[1], val[2], val[3], val[4], stores)
            print(values)
            insertProduct = """INSERT INTO product(product_name,ingredient,quantite,nutrition_grade,url,stores) VALUES('%s','%s','%s','%s','%s','%s') RETURNING id;""" % values
            idProduct = db.sql_insert_id(insertProduct)
            db.sql_request("""INSERT INTO assoc_product_categorie VALUES('%s','%s');""" % (idProduct, idCategorie))

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
            db = Sql(log, confSql)
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
            db.sql_close()
    except KeyboardInterrupt:
        log.warning("Fermeture du programme avec Ctrl+C")
        db.sql_close()

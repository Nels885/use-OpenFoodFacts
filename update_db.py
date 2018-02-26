#! /usr/bin/env python3
# coding: utf-8

import requests
import psycopg2

converDb = {

    'categories_tags': ['categorie', 'name'],
    'product_name': ['product', 'product_name'],
    'ingredients_text_with_allergens_fr': ['product', 'ingredient'],
    'url': ['product', 'url'],
    'nutrition_grades': ['product', 'nutrition_grade'],
    'stores_tags': ['store', 'name']
}


class Sql:

    def __init__(self):
        self.dsn = "dbname=db_OpenFoodFacts user=adm_OFF password=kikoulol port=5432 host=localhost"

    def _psy_exec(self, msgSql):
        try:
            # print("### {} ###".format(msgSql))
            with psycopg2.connect(self.dsn) as conn:
                with conn.cursor() as curs:
                    curs.execute(msgSql)
        except psycopg2.IntegrityError:
            print("### valeur existe ###")

    def sql_insert(self, request):
        self._psy_exec(request)
    # def sql_insert(self, tab, col, val):
    #     self._psy_exec("INSERT INTO %s (%s) VALUES ('%s');" % (tab, col, val))


def data_erase():
    fdb = open('script_erase_DB.sql', 'r')
    sqlFile = fdb.read()
    fdb.close()
    sqlRequest = sqlFile.split(';')
    for req in sqlRequest:
        try:
            db.sql_insert(req)
        except psycopg2.ProgrammingError as err:
            print("requête passé: ", err)


def data_create():
    r = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?search_simple=1&action=process&tagtype_0=countries&tag_contains_0=contains&tag_0=france&sort_by=unique_scans_n&page_size=100&json=1")

    print(r.status_code)
    print(r.headers['content-type'])
    print()

    result = r.json()['products']

    info = ['product_name', 'ingredients_text_with_allergens_fr', 'quantity', 'nutrition_grades', 'url']

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
        values = (val[0], val[1], val[2], val[3], val[4])
        print(values)
        for sto in result[number]['stores_tags']:
            db.sql_insert("""INSERT INTO store(name) VALUES('%s')""" % sto)
        for cat in result[number]['categories_tags']:
            db.sql_insert("""INSERT INTO categorie(name) VALUES('%s')""" % cat)
        db.sql_insert("""INSERT INTO product(product_name,ingredient,quantite,nutrition_grade,url) VALUES('%s','%s','%s','%s','%s')""" % values)


def main():
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
          "~~     Mise à jour Base de données     ~~\n"
          "~~            Pure Beurre              ~~\n"
          "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
          "\n"
          "Listes des options:\n"
          " 1 - Effacez la base de données\n"
          " 2 - Insérez données dans la base de données\n")
    return input("Entrez le numéro de votre choix ( ou <Enter> pour quitter) : ")


if __name__ == '__main__':
    db = Sql()
    choice = main()
    if choice == "1":
        data_erase()
    elif choice == "2":
        data_create()

"""
Database management module
"""

import psycopg2


class Database:

    def __init__(self, log, confSql):
        self.log = log
        dbname = confSql['dbname']
        user = confSql['user']
        password = confSql['password']
        port = confSql['port']
        host = confSql['host']
        dsn = "dbname='{}' user='{}' password='{}' port='{}' host='{}'".format(dbname, user, password, port, host)
        try:
            self.conn = psycopg2.connect(dsn)
            self.curs = self.conn.cursor()
        except psycopg2.OperationalError as err:
            self.log.error("Accès base de données: %s", err)
            self.close()

    def execute(self, request, param=None):
        if request not in ['', None]:
            try:
                self.curs.execute(request, param)
            except Exception as err:
                self.log.warning("### Requêtes SQL incorrecte : %s\n"
                                 "Erreur : %s ###", (request, err))
            self.commit()

    def insert_id(self, request):
        if request not in ['', None]:
            id = None
            try:
                self.execute(request)
                id = self.curs.fetchone()[0]
            except TypeError:
                id = None
            self.commit()
            return id

    # def sql_insert(self, table, colomn, value):
    #     insert = """INSERT INTO {}({}) VALUES('%s');""".format(table, colomn)
    #     self.execute(insert % value)

    def result(self):
        return self.curs.fetchall()

    def select(self, request):
        self.execute(request)
        return self.result()

    def sql_script(self, sqlFile):
        self.execute(open(sqlFile, 'r').read())

    def commit(self):
        if self.conn:
            self.conn.commit()

    def close(self):
        if self.conn:
            self.conn.close()

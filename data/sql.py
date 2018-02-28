"""
SQL request module
"""

import psycopg2


class Sql:

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
            self.sql_close()

    def sql_request(self, request):
        if request not in ['', None]:
            try:
                self.curs.execute(request)
            except psycopg2.IntegrityError as err:
                self.log.warning("### valeur existe: %s ###", err)
            self.conn.commit()

    def sql_insert_id(self, request):
        if request not in ['', None]:
            id = None
            try:
                self.curs.execute(request)
                id = self.curs.fetchone()[0]
            except psycopg2.IntegrityError as err:
                self.log.warning("### valeur existe: %s ###", err)
            except TypeError:
                id = None
            self.conn.commit()
            return id

    def sql_insert(self, table, colomn, value):
        insert = """INSERT INTO {}({}) VALUES('%s');""".format(table, colomn)
        self.sql_request(insert % value)

    def sql_select(self, request):
        self.curs.execute(request)
        result = self.curs.fetchall()
        self.conn.commit()
        return result

    def sql_script(self, sqlFile):
        self.sql_request(open(sqlFile, 'r').read())

    def sql_close(self):
        self.conn.commit()
        self.curs.close()
        self.conn.close()






    # def _psy_exec(self, msgSql):
    #     idInsert = None
    #     try:
    #         with psycopg2.connect(self.dsn) as conn:
    #             with conn.cursor() as curs:
    #                 curs.execute(msgSql)
    #                 idInsert = curs.fetchone()[0]
    #     except psycopg2.IntegrityError:
    #         self.log.warning("### valeur existe ###")
    #     except psycopg2.ProgrammingError as err:
    #         self.log.warning("requête passé: %s", err)
    #     except psycopg2.OperationalError as err:
    #         self.log.error("Accès base de données: %s", err)
    #     except TypeError:
    #         idInsert = None
    #     return idInsert
    #
    # def _spy_selec(self, msgSql):
    #     result = None
    #     try:
    #         with psycopg2.connect(self.dsn) as conn:
    #             with conn.cursor() as curs:
    #                 curs.execute(msgSql)
    #                 result = curs.fetchone()
    #     except psycopg2.IntegrityError:
    #         self.log.warning("### valeur existe ###")
    #     except psycopg2.ProgrammingError as err:
    #         self.log.warning("requête passé: %s", err)
    #     except psycopg2.OperationalError as err:
    #         self.log.error("Accès base de données: %s", err)
    #
    #     return result
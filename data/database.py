"""
Database management module
"""

import psycopg2


class Database:

    SELECT = """SELECT %s FROM %s"""
    WHERE = """ WHERE %s"""

    def __init__(self, log, confSql):
        """
        ## Initialize Class Database ##
            :param log: logging module
            :param confSql: dict of parameters for the configuration of the Database
        """
        self.log = log
        dbname = confSql['dbname']
        user = confSql['user']
        password = confSql['password']
        port = confSql['port']
        host = confSql['host']
        dsn = "dbname='{}' user='{}' password='{}' port='{}' host='{}'".format(dbname, user, password, port, host)
        try:
            self.conn = psycopg2.connect(dsn)
        except psycopg2.OperationalError as err:
            self.log.error("Accès base de données: %s", err)
            self.error = True
        else:
            self.curs = self.conn.cursor()
            self.error = False

    def execute(self, request, param=None):
        """
        ## Execute the requests SQL ##
            :param request:
            :param param:
            :return: commit() method
        """
        if request not in ['', None]:
            try:
                self.curs.execute(request, param)
            except Exception as err:
                self.log.warning("### Requêtes SQL incorrecte : %s\n"
                                 "Erreur : %s ###" % (request, err))
            self.commit()

    def insert_id(self, request):
        try:
            self.execute(request)
            id = self.curs.fetchone()[0]
        except TypeError:
            id = None
        self.commit()
        return id

    def result(self):
        """
        ## Result of the request SQL ##
            :return: return the result from of a list of tuple
        """
        return self.curs.fetchall()

    def select(self, colomns, tables, cond=None, param=None, condition=False):
        """
        ## Select Method used by 'purebeurre_client.py' program##
            :param colomns: the colomns to display
            :param tables: the selected tables
            :param cond: the condition for the SELECT
            :param param: the values for the condition
            :param condition: Activation of the condition
            :return: result of the result() method
        """
        if condition:
            req = self.SELECT + self.WHERE + ";"
            req = req % (colomns, tables, cond)
        else:
            req = self.SELECT + ";"
            req = req % (colomns, tables)
        self.log.info("## %s ##", req)
        self.execute(req, param)
        return self.result()

    def sql_script(self, sqlFile):
        """
        ## Execute script SQL file ##
            :param sqlFile: file to execute
            :return: execute the different SQL requests in the file
        """
        self.execute(open(sqlFile, 'r').read())

    def commit(self):
        """
        ## Validation SQL requests ##
            :return: Validate the latest SQL requests that are in the Random Access Memory
        """
        if not self.error:
            if self.conn:
                self.conn.commit()

    def close(self):
        """
        ## Close database ##
            :return: Closing of the connection with the database
        """
        if not self.error:
            if self.conn:
                self.conn.close()

"""
Database management module
"""

import psycopg2


class Database:
    SELECT = "SELECT %s FROM %s"
    WHERE = " WHERE %s"
    INSERT = "INSERT INTO %s"
    COLUMNS = "(%s)"
    VALUE = " VALUES("
    RETURN_ID = " RETURNING id;"

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

    def insert(self, table, param, columns=None, returnId=False):
        """
        ## inserting values into a table ##
            :param table: table in which we want to insert the values
            :param param: values to insert
            :param columns: columns in which we want to insert the values
            :param returnId: valid if we want the ID of the line
            :return: value of the ID
        """
        values = "%s," * len(param)
        if columns is None:
            insert = self.INSERT % table
        else:
            insert = (self.INSERT + self.COLUMNS) % (table, columns)
        req = insert + self.VALUE + values[:-1] + ");"
        idLine = self.__return_id(req, param, returnId)
        return idLine

    def select(self, columns, tables, cond=None, param=None, condition=False):
        """
        ## Select Method used by 'purebeurre_client.py' program##
            :param columns: the colomns to display
            :param tables: the selected tables
            :param cond: the condition for the SELECT
            :param param: the values for the condition
            :param condition: Activation of the condition
            :return: result of the result() method
        """
        if condition:
            req = self.SELECT + self.WHERE + ";"
            req = req % (columns, tables, cond)
        else:
            req = self.SELECT + ";"
            req = req % (columns, tables)
        self.log.debug("## %s ##", req)
        self._execute(req, param)
        return self.__result()

    def sql_script(self, sqlFile):
        """
        ## Execute script SQL file ##
            :param sqlFile: file to execute
            :return: execute the different SQL requests in the file
        """
        self._execute(open(sqlFile, 'r').read())

    def close(self):
        """
        ## Close database ##
            :return: Closing of the connection with the database
        """
        if not self.error:
            if self.conn:
                self.conn.close()

    def _execute(self, request, param=None):
        """
        ## Execute the requests SQL ##
            :param request:
            :param param:
            :return: commit() method
        """
        try:
            self.curs.execute(request, param)
        except Exception as err:
            self.log.debug("### Requêtes SQL incorrecte : %s\n"
                             "Erreur : %s ###" % (request, err))
        self._commit()

    def _commit(self):
        """
        ## Validation SQL requests ##
            :return: Validate the latest SQL requests that are in the Random Access Memory
        """
        if not self.error:
            if self.conn:
                self.conn.commit()

    def __return_id(self, request, param, returnId):
        """
        ## return the ID of the line, if it's requested ##
            :param request: request SQL
            :param param: values for the request
            :param returnId: valid if we want the ID of the line
            :return: value of the ID
        """
        idLine = None
        if returnId:
            req = request[:-1] + self.RETURN_ID
            self._execute(req, param)
            idLine = self.curs.fetchone()[0]
        else:
            self._execute(request, param)
        return idLine

    def __result(self):
        """
        ## Result of the request SQL ##
            :return: return the result from of a list of tuple
        """
        return self.curs.fetchall()

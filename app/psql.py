import os
import sys

import psycopg2
from psycopg2 import extras

from app.config import TABLE_NAME, TABLE_COLUMNS,PSQL_USER,PSQL_PORT,PSQL_DB,DATABASE_URL,PSQL_PASSWORD

import os,logging
 
logger = logging.getLogger(os.path.basename(__file__))

class PSQL:
    """
    A singleton connection class
    """
    __conn = None

    def __init__(self):
        if PSQL.__conn is not None:
            raise Exception("Should not happen!")
        else:
            # creating psql connection.
            conn = self._psql_connection()
            PSQL.__conn = conn

    @staticmethod
    def get_instance():
        """
        Singleton method.
        """
        if PSQL.__conn is None:
            PSQL()
        return PSQL.__conn

    def _psql_connection(self):
        """
        :return: Creates and returns DB connection object
        """
        psql_credentials = {
            'database': PSQL_DB,
            'user': PSQL_USER,
            'password': PSQL_PASSWORD,
            'host': DATABASE_URL,
            'port': int(PSQL_PORT)
        }
        try:
            # connecting to psql server
            connection = psycopg2.connect(**psql_credentials, sslmode='require')
            logger.info("Database connected")
            
        except Exception as e:
            logger.info("Error while connecting to DB - {}".format(e))
            sys.exit()

        return connection


class MiddleLayer:
    """
    Middleman between DB and main function
    """

    def __init__(self):
        self.conn = PSQL.get_instance()
        self.cur = self.conn.cursor()

    def add_record(self, add_record, table=TABLE_NAME):

        #insert if all well, rollback on some error
        insert_query = "INSERT INTO {}{} VALUES %s".format(table, TABLE_COLUMNS)
        try:
            extras.execute_values(self.cur, insert_query, [add_record])
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()

    def search_query(self, query, table=TABLE_NAME, limit=5):

        cursor = self.conn.cursor(cursor_factory=extras.DictCursor)
        cursor.execute("SELECT content, created_by FROM {} WHERE content like '%{}%' order by created_at DESC LIMIT {};".format(table, query, limit))
        result = cursor.fetchall()
        cursor.close()
        return result

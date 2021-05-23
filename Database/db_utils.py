import configparser as cp
import mysql.connector
import os

''' database configuration parser and connections '''
parser = cp.SafeConfigParser()
parser.read(os.getcwd()+'\Database\db.ini')


host = parser.get('database_congfiguration_details', 'host')
user = parser.get('database_congfiguration_details', 'user')
password = parser.get('database_congfiguration_details', 'password')
database = parser.get('database_congfiguration_details', 'database')


class Database_Connection:
    def __init__(self):
        self.__host = host
        self.__user = user
        self.__password = password
        self.__database = database
        self.mydatabase = self.__dababase_instance()

    def __del__(self):
        return True

    def __dababase_instance(self):
        return mysql.connector.connect(host=self.__host, user=self.__user, password=self.__password, database=self.__database)

    def _connect_database(self):
        return self.mydatabase

    def _disconnect_database(self):
        self.mydatabase.close()
        self.__del__()

    def _select_query(self, query):
        cursor = self.mydatabase.cursor()
        cursor.execute(query)
        return list(cursor.fetchall())

    def _insert_query(self, query):
        cursor = self.mydatabase.cursor()
        cursor.execute(query)
        self.mydatabase.commit()

    def _delete_query(self, query):
        cursor = self.mydatabase.cursor()
        cursor.execute(query)
        self.mydatabase.commit()

    def _update_query(self, query):
        cursor = self.mydatabase.cursor()
        cursor.execute(query)
        self.mydatabase.commit()

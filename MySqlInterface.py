# --------------------------------------------------
# This file contains an interface to a MySql database
#
# (C) 2020 Esipov Paul
# Distributed under GNU public license
# email: esipov.p@mail.ru
# --------------------------------------------------
import mysql.connector as mysql_c
from Config import Config


class MySqlConn:
    """ Class implements mysql database interface
    This class is a singleton
    """
    __singleton = None
    __is_db_connected = False
    __connector = None
    __cursor = None

    def __new__(cls, *args, **kwargs):
        if not cls.__singleton:
            cls.__singleton = super(MySqlConn, cls).__new__(cls, *args, **kwargs)
        return cls.__singleton

    def set_db_conn(self):
        """ Sets connection with database using parameters set in the configuration file
        for details, see description of the Config class

        :return: None
        """
        self.__connector = mysql_c.connect(
            user=Config().get_database_user(),
            password=Config().get_database_pass(),
            host=Config().get_database_address(),
            database=Config().get_database_name()
        )

        self.__cursor = self.__connector.cursor()
        return None

    def db_conn_check(self):
        if not self.__is_db_connected:
            self.set_db_conn()

    def store_concert(self, concert_meta):
        """ Calls procedure stored in MySql database to save concert description to database

        :param concert_meta: (string) json string containing event metadata
        :return: None
        """
        self.db_conn_check()
        return None

# --------------------------------------------------
# This file contains an interface to a MySql database
#
# (C) 2020 Esipov Paul
# Distributed under GNU public license
# email: esipov.p@mail.ru
# --------------------------------------------------
from sqlalchemy import create_engine
import pymysql
from Config import Config
import pandas as pd


class MySqlConn:
    """ Class implements mysql database interface
    This class is a singleton
    """
    __singleton = None
    __is_db_connected = False
    __mysql_engine = None
    __mysql_conn = None

    def __new__(cls, *args, **kwargs):
        if not cls.__singleton:
            cls.__singleton = super(MySqlConn, cls).__new__(cls, *args, **kwargs)
        return cls.__singleton

    def get_server_version(self):
        mysql_version_info = self.__mysql_conn.execute('SELECT VERSION()')
        if mysql_version_info.rowcount != 0:
            print('Successfully connected mysql server:')
            for row in mysql_version_info:
                print(f'  mysql version = {row[0]}\n')

    def set_db_conn(self):
        """ Sets connection with database using parameters set in the configuration file
        for details, see description of the Config class

        :return: None
        """
        self.__mysql_engine = create_engine(f'{Config().get_database_type()}+pymysql://'
                                            f'{Config().get_database_user()}:{Config().get_database_pass()}@'
                                            f'{Config().get_database_address()}/{Config().get_database_name()}')
        self.__mysql_conn = self.__mysql_engine.connect()

        # To test connection, output mysql server version
        self.get_server_version()
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


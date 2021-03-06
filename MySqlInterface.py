# --------------------------------------------------
# This file contains an interface to a MySql database
#
# (C) 2020 Esipov Paul
# Distributed under GNU public license
# email: esipov.p@mail.ru
# --------------------------------------------------
from sqlalchemy import create_engine
from sqlalchemy import exc
from sqlalchemy.orm import sessionmaker
from Config import Config
import pandas as pd
import sys


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
            cls.__singleton.set_db_conn()
        return cls.__singleton

    def get_server_version(self):
        """ Prints and returns
        version of a connected mysql server

        :return: (string) mysql version string
        """
        mysql_version_info = self.__mysql_conn.execute('SELECT VERSION()')
        if mysql_version_info.rowcount != 0:
            for row in mysql_version_info:
                return row[0]
        return None

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
        if not self.__is_db_connected:
            print('Successfully connected mysql server:')
            self.get_server_version()
            self.__is_db_connected = True

        return None

    def db_conn_check(self):
        """ Checks connection with database

        :return: (bool) connection active : TODO
        """
        if not self.__is_db_connected:
            self.set_db_conn()

    def is_event_inserted(self, event_name):
        """ Checks if event is in event table

        :param event_name: (string) name of the event to check
        :return: (bool) is event in table
        """
        is_found = False
        try:
            self.db_conn_check()
            search_res = self.__mysql_conn.execute(f'SELECT * FROM t_event WHERE name = \'\"{event_name}\"\'')
            if search_res.rowcount != 0:
                is_found = True
        except:
            e = sys.exc_info()
            print(f'sql insertion exception: {e}')
        finally:
            return is_found

    def store_concert(self, concert_object):
        """ Calls procedure stored in MySql database to save concert description to database

        :param concert_object: (string) Concert event class object. See EventClass.py
        :return: None
        """
        try:
            self.__mysql_conn.execute(f'CALL StoreConcertInBuff'
                                      f'(\'{concert_object.to_json()}\');')
        except:
            e = sys.exc_info()
            print(f'sql insertion exception: {e}')
        finally:

            return None

    def db_process_events(self):
        try:
            self.__mysql_conn.execute(f'CALL CursorIterator();')
        except:
            e = sys.exc_info()
            print(f'sql insertion exception: {e}')
        finally:

            return None

    def get_event_tab(self):
        """ Selects the whole t_event table, converts it to a pd.dataframe
        abd returns this dataframe

        :return: (pandas dataframe) select * from t_event tab in fyw_db
        """
        return pd.read_sql("CALL GetEventTab()", con=self.__mysql_conn)

# --------------------------------------------------
# This file contains interface to the xml config file
#
#
# (C) 2020 Esipov Paul
# Distributed under GNU public license
# email: esipov.p@mail.ru
# --------------------------------------------------
import xml.etree.ElementTree as ET


class Config:
    """ Interface class to the xml configuration file
        This class is a singleton

    """
    config_tree = ET.parse("config.xml")
    config_tree_root = config_tree.getroot()
    __singleton = None

    def __new__(cls, *args, **kwargs):
        if not cls.__singleton:
            cls.__singleton = super(Config, cls).__new__(cls, *args, **kwargs)
        return cls.__singleton

    def get_database_type(self):
        """ get type of the database used.
        Possible options:
            - sqlite
            - postgresql (not adapted)
            - mysql      (not adapted)

        :return: (string) type of database
        """
        return self.config_tree_root.find("./database/type").text

    def get_database_name(self):
        """ get name of the database, or a database file name if sqlite
        :return: (string) database name
        """
        return self.config_tree_root.find("./database/db_name").text

    def get_table_name(self, table_type):
        """ Get name of a database table

        :param table_type: (string) type of table for which name is searched
        :return: (string) name of table
        """
        return self.config_tree_root.find(f'./database/tables/item[@name="{table_type}"]/table_name').text

    def get_table_columns_list(self, table_type):
        """ Get list if column names in specified table

        :param table_type: (string) type of table
        :return: (string list) list of table columns
        """
        return [c_name.text for c_name in self.config_tree_root.findall(
            f'./database/tables/item[@name="{table_type}"]/columns/item'
        )]

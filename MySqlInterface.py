# --------------------------------------------------
# This file contains an interface to a MySql database
#
# (C) 2020 Esipov Paul
# Distributed under GNU public license
# email: esipov.p@mail.ru
# --------------------------------------------------
import mysql.connector as mysql_c


def mysql_database_connect():
    """ Establish connection with MySql database

    :return: (bool): connection established
    """
    return True


def upload_concert(concert_json_str):
    """ Upload concert event metadata to database

    :param concert_json_str: json string containing concert event metadata
    :return:
    """
    return None

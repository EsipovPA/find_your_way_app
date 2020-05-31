# --------------------------------------------------
# This file contains sqlite interface functions such as:
#   Checking database connection
#
#   Uploading data to sqlite db from:
#       json, xml structures into database tables
#
#   Getting data from sqlite tables and converting it into:
#       json, xml structures
#       pandas data frames
#
# (C) 2020 Esipov Paul
# Distributed under GNU public license
# email: esipov.p@mail.ru
# --------------------------------------------------
import pandas as pd
import sqlite3
import json
from Config import Config


def upload_json(json_str, db_table):
    """ Upload json structure to user-defined table

    :param json_str: (json) input data in json formatted string
    :param db_table: (string) table to upload the data
    :return: None
    """
    print("\nIn the upload_json")

    try:
        conn = sqlite3.connect(Config().get_database_name())
        cursor = conn.cursor()
        input_data = json.loads(json_str)
        # Unpack json data and upload to different tables
        
    except sqlite3.Error as e:
        print(f"  database connection error: {e}")
    finally:
        conn.close()

    print("End of the uload_json\n")
    return None

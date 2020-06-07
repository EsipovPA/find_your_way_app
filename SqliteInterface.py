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
from EventClass import Event


def upload_event(event):
    """ Upload event structure

    :param event: Event class object, or one of it's subclasses
    :return:
    """


    return None


def upload_json(json_str):
    """ Upload json structure

    :param json_str: (json) input data in json formatted string
    :param db_table: (string) table to upload the data
    :return: None
    """
    print("\nIn the upload_json")

    try:
        conn = sqlite3.connect(Config().get_database_name())
        cursor = conn.cursor()
        input_data = json.loads(json_str)

        event_id = get_event_id(input_data['name'], cursor)
        if event_id is None:
            print(f"Create new event: {input_data['name']}")

        # update event data is other tables
        print(f"artists = {input_data['artists'][0]}")
    except sqlite3.Error as e:
        print(f"  database connection error: {e}")
    finally:
        conn.close()

    print("End of the upload_json\n")
    return None


def upload_xml(xml_str):
    """

    :param xml_str: (string) input data in xml formatted string
    :return:
    """
    return None


def get_event_id(event_name, cursor):
    """ Get event identifier form database. Return None if event does not exist in database

    :param event_name: (string) name of the event to search in database
    :param cursor: sqlite cursor connected to the database
    :return: (bool) event found in database
    """
    cursor.execute(f"SELECT * FROM event WHERE "
                   f"{Config().get_table_columns_list(table_type='event')[1]}=\"{event_name}\"")
    return cursor.fetchone()[0]


def update_artist_data(cursor, artist_name, event_name):
    """ If artist does not appear in database, create new artist record.
    Set connection between artist and event

    :param cursor: sqlite cursor
    :param artist_name: (string) name of the artist
    :param event_name: (string) name of the event, that the artist participates
    :return: None
    """
    print(f"select * from {Config().get_table_name('artist')}"
                   f"where {Config().get_table_columns_list('artist')[2]}=\"{artist_name}\"")
    cursor.execute(f"select * from {Config().get_table_name('artist')}"
                   f"where {Config().get_table_columns_list('artist')[2]}=\"{artist_name}\"")
    print(f"size of the request result = {len(cursor.fetchall())}")
    return None


def update_genre_data(cursor, genre_name, event_name):
    """ If genre does not appear in database, create new genre record.
    Set connection between genre and event if is not set

    :param cursor:
    :param genre_name:
    :param event_name:
    :return:
    """
    return None


def update_address_data(cursor, genre_name, event_name):
    return None


def update_location_data(cursor, location_name, event_name):
    return None

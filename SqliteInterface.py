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
from EventClass import Concert


def upload_concert(concert):
    """ Upload concert structure

    :param concert: Event class object, or one of it's subclasses
    :return:
    """
    print("In the upload_event")

    try:
        conn = sqlite3.connect(Config().get_database_name())
        cursor = conn.cursor()

        event_id = get_event_id(concert.name, cursor)
        if event_id is None:
            event_id = insert_new_event(conn, event_name=concert.name)

        for artist in concert.artists:
            update_artist_data(conn, artist, event_id)
    except sqlite3.Error as e:
        print(f"  database connection error: {e}")
    finally:
        conn.close()

    return None


def get_event_id(event_name, cursor):
    """ Get event identifier form database. Return None if event does not exist in database

    :param event_name: (string) name of the event to search in database
    :param cursor: sqlite cursor connected to the database
    :return: (bool) event found in database
    """
    cursor.execute(f"SELECT * FROM event WHERE "
                   f"{Config().get_table_columns_list(table_type='event')[1]}=\"{event_name}\"")
    if cursor.fetchone() is None:
        return None
    else:
        return cursor.fetchone()[0]


def update_artist_data(connection, artist_name, event_id):
    """ If artist does not appear in database, create new artist record.
    Set connection between artist and event

    :param connection: sqlite connection object
    :param artist_name: (string) name of the artist
    :param event_id: (int) event identifier in the database
    :return: None
    """
    cursor = connection.cursor()
    cursor.execute(f"select * from {Config().get_table_name('artist')} "
                   f"where {Config().get_table_columns_list('artist')[2]} = {artist_name}")

    artist_record = cursor.fetchone()
    if artist_record is None:
        cursor.execute(f"insert into {Config().get_table_name('artist')} "
                       f"({', '.join(Config().get_table_columns_list('artist'))}) "
                       f"values ({', '.join([new_artist_id(connection), artist_name])})")
        connection.commit()

    # TODO: Update artist - event relation table
    # cursor.execute(f"select * from {Config().get_table_name('event_artist')} "
    #                f"where")

    connection.commit()
    return None


def new_artist_id(connection):
    """ generate new artist id

    :param connection: sqlite connection object
    :return: new artist id
    """
    cursor = connection.cursor()
    cursor.execute(f"select * from {Config().get_table_name('artist')} order by id desc limit 1")
    last_artist_rec = cursor.fetchone()
    if last_artist_rec is None:
        return 1
    else:
        return last_artist_rec[0] + 1


def insert_new_event(conn, event_name):
    """ 1) Generate new event ID
    2) insert event data into table 'event'

    :param conn: sqlite connection
    :param event_name: (string) name of the event
    :return: (int) new event identifier
    """
    event_name = f'"{event_name}"'
    cursor = conn.cursor()
    cursor.execute(f"select * from {Config().get_table_name('event')}"
                   f" order by {Config().get_table_columns_list('event')[0]} desc limit 1")
    last_event = cursor.fetchone()
    if last_event is not None:
        new_event_id = last_event[0] + 1
        cursor.execute(f"insert into {Config().get_table_name('event')} "
                       f"({', '.join(Config().get_table_columns_list('event'))}) "
                       f"values ({', '.join([str(new_event_id), event_name])})")
    else:
        new_event_id = 1
    conn.commit()
    return new_event_id


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

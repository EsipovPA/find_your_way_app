# --------------------------------------------------
# Main file of the afisha web site scraper
#
# (C) 2020 Esipov Paul
# Distributed under GNU public license
# email: esipov.p@mail.ru
# --------------------------------------------------
from ScanConsert import get_concert_list, get_concert_object
from MySqlInterface import MySqlConn
import time


# Get concert metadata
concert_list = get_concert_list()
concert_obj_list = []

# Insert all concerts
print(f'concert count = {len(concert_list)}')
counter = 0
for link in concert_list:
    c_obj = get_concert_object(concert_link=link)
    print(f'{counter} -> {c_obj.link}')
    MySqlConn().store_concert(concert_object=c_obj)
    counter += 1

print("I'm done")

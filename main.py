# --------------------------------------------------
# Main file of the afisha web site scraper
#
# (C) 2020 Esipov Paul
# Distributed under GNU public license
# email: esipov.p@mail.ru
# --------------------------------------------------
from ScanConsert import get_concert_list, get_concert_object
from MySqlInterface import MySqlConn

# Debug special character processing using url: https://www.afisha.ru/concert/2013655/
# debug_meta = get_concert_object('https://www.afisha.ru/concert/2012335/').to_json()
# print(f'debug meta = {debug_meta}')


# Get concert metadata
concert_list = get_concert_list()

# Insert all concerts
print(f'concert count = {len(concert_list)}')
counter = 0
for link in concert_list:
    c_obj = get_concert_object(concert_link=link)
    MySqlConn().store_concert(concert_meta=c_obj.to_json())
    counter += 1

print("I'm done")

# --------------------------------------------------
# Main file of the afisha web site scraper
#
# (C) 2020 Esipov Paul
# Distributed under GNU public license
# email: esipov.p@mail.ru
# --------------------------------------------------
from ScanConsert import get_concert_list, get_concert_meta, get_concert_object
from SqliteInterface import upload_concert
from Config import Config
from EventClass import Concert, Event


# Get concert metadata
concert_list = get_concert_list(pages_limit=1)

# test_concert_meta = get_concert_object(concert_link=concert_list[0])
# std_time_str = get_std_time_str(test_concert_meta.time)

# concert_meta = [get_concert_object(concert_link=link) for link in concert_list]

# first_concert = get_concert_object(concert_link=concert_list[0])
# print(f"concert meta = {first_concert.to_json()}")
# upload_concert(first_concert)

print("I'm done")

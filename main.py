# --------------------------------------------------
# Main file of the afisha web site scraper
#
# (C) 2020 Esipov Paul
# Distributed under GNU public license
# email: esipov.p@mail.ru
# --------------------------------------------------
from ScanConsert import get_concert_list, get_concert_meta
from SqliteInterface import upload_json
from Config import Config


# Get concert metadata
concert_list = get_concert_list(pages_limit=1)
first_concert_meta = get_concert_meta(concert_link=concert_list[0], meta_format="json")

upload_json(first_concert_meta)

print("I'm done")

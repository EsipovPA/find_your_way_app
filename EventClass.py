# --------------------------------------------------
# This file contains the description of Event class
# and all the subclasses of Event class such as:
#   Event
#   Concert
#   Theater
#
# (C) 2020 Esipov Paul
# Distributed under GNU public license
# email: esipov.p@mail.ru
# --------------------------------------------------
import json


def get_meta_string(input_string):
    """ Function deletes all split symbols

    :param input_string: (string) standard string
    :return: (string) string with only words
    """
    return " ".join(input_string.split())


class Event:
    """Basic class of the afisha event

    """
    def __init__(self):
        self.name = str("")         # +
        self.label = str("")        # +
        self.link = str("")         # +
        self.location = str("")     # +
        self.time = str("")         # +
        self.json_data = {}         # +
        self.description_tags = []  # -
        self.description = str("")  # +

    def parse_page(self, page_soup):
        # Get event label
        self.label = page_soup.select("title")[0].getText().split(",")[0]

        # Get event name
        widget_header = page_soup.select(".info-widget__header")
        if len(widget_header) != 0:
            self.name = get_meta_string(widget_header[0].getText())

        # Get event location
        widget_location = page_soup.findAll("div", itemprop="location")
        if len(widget_location) != 0:
            loc_search = widget_location[0].findAll("label", itemprop="streetAddress")
            if len(loc_search) != 0:
                self.location = loc_search[0].getText()

        # Get event time
        widget_time = page_soup.select(".meta___1n6MI")
        self.time = widget_time[0].findAll("span")[-1].getText()

        # Get event search tags
        self.description = page_soup.findAll(itemprop="description")[0].getText()
        # self.description_tags = get_description_search_tags(self.description)

    def set_event_link(self, link_str):
        self.link = link_str

    def to_json(self):
        self.json_data["name"] = self.name
        self.json_data["label"] = self.label
        self.json_data["link"] = self.link
        self.json_data["location"] = self.location
        self.json_data["time"] = self.time
        return json.dumps(self.json_data, ensure_ascii=False)

    def get_description(self):
        return self.description


class Concert(Event):
    def __init__(self):
        super().__init__()
        self.artists = []
        self.genres = []

    def parse_page(self, page_soup):
        # Read event parameters
        super().parse_page(page_soup)

        # Get concert genre
        widget_genres = page_soup.select(".info-widget__meta")
        if len(widget_genres) != 0:
            find_genre = widget_genres[0].find_all('a')
        for fg in find_genre:
            self.genres.append(fg.getText())

        # Get concert artists
        widget_artists = page_soup.select(".other-actors")
        if len(widget_artists) != 0:
            artist_search = widget_artists[0].select(".object__block-content")
            if len(artist_search) != 0:
                artist_string = get_meta_string(artist_search[0].getText())
                self.artists = artist_string.split(', ')

    def to_json(self):
        super().to_json()
        self.json_data["artists"] = ", ".join(self.artists)
        self.json_data["genres"] = ", ".join(self.genres)
        return json.dumps(self.json_data, ensure_ascii=False)

    def to_string(self):
        return ", ".join([self.name, self.link, self.location, self.artists[0]])


class Theater(Event):
    def __init__(self):
        super().__init__()
        self.director = str("")
        self.theater_name = str("")

    def to_json(self):
        json_string = ""
        return json_string

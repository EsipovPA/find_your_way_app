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
from xml.etree.ElementTree import ElementTree, Element, SubElement, Comment, tostring
import xml.dom.minidom as xdm
from Regex import get_std_time_str


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
        self.name = str("")                     # Event name
        self.label = str("")                    # Event label from event web-page
        self.link = str("")                     # Link to the event web-page
        self.location = str("")                 # Location of the event
        self.time = str("")                     # Event time
        self.json_data = {}                     # Event metadata converted into json format
        self.description = str("")              # Text description of the event

        self.xml_data = Element("metadata")     # TODO: xml metadata output
        self.xml_data.set("version", "1.0")     # TODO: xml metadata output

    def parse_page_soup(self, page_soup):
        """ Get event metadata from event web page at afisha-moscow

        :param page_soup: (bs4) event page soup
        :return: None
        """
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
        widget_time = page_soup.select("._2YgOJ")   # fix may be needed
        self.time = get_std_time_str(widget_time[0].findAll("span")[-1].getText())

        # Get event description
        self.description = page_soup.findAll(itemprop="description")[0].getText()

    def set_event_link(self, link_str):
        """ Set link to event web page

        :param link_str: (string) event link string
        :return: None
        """
        self.link = link_str

    def to_json(self):
        """ Convert event metadata into json string

        :return: (string) event metadata in json format
        """
        self.json_data["name"] = self.name
        self.json_data["label"] = self.label
        self.json_data["link"] = self.link
        self.json_data["location"] = self.location
        self.json_data["time"] = self.time
        self.json_data["description"] = self.description
        return json.dumps(self.json_data, ensure_ascii=False)

    def to_xml(self):
        """ Convert event metadata to xml string

        :return: (string) event metadata in xml format
        """
        SubElement(self.xml_data, "name").text = self.name
        SubElement(self.xml_data, "label").text = self.label
        SubElement(self.xml_data, "link").text = self.link
        SubElement(self.xml_data, "location").text = self.location
        SubElement(self.xml_data, "time").text = self.time
        SubElement(self.xml_data, "description").text = self.description

        print(f"test xml output:\n{self.xml_data.text}")

        dom = xdm.parseString(self.xml_data.text)
        return dom.toprettyxml()

    def get_description(self):
        return self.description


class Concert(Event):
    def __init__(self):
        super().__init__()
        self.artists = []
        self.genres = []

    def parse_page_soup(self, page_soup):
        """ Get concert metadata from bs4 event page object

        :param page_soup: (bs4) event page soup
        :return: None
        """
        # Read event parameters
        super().parse_page_soup(page_soup)

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
        """ Output event metadata in json string

        :return: (json string) concert metadata
        """
        super().to_json()
        self.json_data["artists"] = ", ".join(self.artists)
        self.json_data["genres"] = ", ".join(self.genres)
        return json.dumps(self.json_data, ensure_ascii=False)

    def to_string(self):
        """ Get Concert name, link, location and first artist
        in a string format, separated by commas

        :return: (string)
        """
        return ", ".join([self.name, self.link, self.location, self.artists[0]])

    def to_xml(self):
        """ Build xml string from concert metadata

        :return: (xml string) concert metadata
        """
        super().to_xml()
        SubElement(self.xml_data, "artists").text = ", ".join(self.artists)
        SubElement(self.xml_data, "genres").text = ", ".join(self.genres)
        dom = xdm.parseString(self.xml_data)
        return dom.toprettyxml()


class Theater(Event):
    def __init__(self):
        super().__init__()
        self.director = str("")
        self.theater_name = str("")

    def to_json(self):
        json_string = ""
        return json_string

    def to_xml(self):
        return "xml string"

# --------------------------------------------------
# This file contains functions that get list of concert pages
# From main concert list on afisha moscow website
#
# (C) 2020 Esipov Paul
# Distributed under GNU public license
# email: esipov.p@mail.ru
# --------------------------------------------------
import requests
from bs4 import BeautifulSoup
from EventClass import Concert


def get_widget_content(page_soup):
    """ Need to find a way to get pages object automatically.

    :param page_soup: (bs4 object) concert schedule list page
    :return: (string list) object containing pages links
    """
    return page_soup.select(".OW6DD")       # Look at website and check if does not work


def get_concert_list(pages_limit=None):
    """ Gets list of concerts for afisha moscow website

    :param pages_limit: (int) limit of concert list pages to scan. Initially - None
    :return: (string list) list of concert links
    """
    concert_list = []

    res = requests.get('https://www.afisha.ru/msk/schedule_concert/?view=list')
    soup = BeautifulSoup(res.text, 'lxml')
    pages_links_set = []

    widget_content = get_widget_content(soup)

    pages_links_widget = widget_content[0].findAll('a', href=True)
    pages_count = int(pages_links_widget[int(len(pages_links_widget) - 2)].getText())
    for p in range(2, pages_count + 1):
        pages_links_set.append('https://www.afisha.ru/msk/schedule_concert/page' + str(p) + '/?view=list')

    print("Get concert links set")
    page_counter = 0
    for page_link in pages_links_set:
        page_counter += 1
        page_request = requests.get(page_link)
        page_soup = BeautifulSoup(page_request.text, 'lxml')
        list_widget = page_soup.select('.content')
        if len(list_widget) != 0:
            list_items = list_widget[0].select('.new-list__item-info')
            print(f"pages scanned = {page_counter}")
            if len(list_items) != 0:
                links_list = []
                for item in list_items:
                    link = item.findAll('a', href=True)
                    if len(link) != 0:
                        concert_list.append("https://www.afisha.ru" + link[0]['href'])

            if pages_limit is not None and pages_limit == page_counter:
                break

    return concert_list


available_meta_formats = ["json", "xml"]


def get_concert_meta(concert_link, meta_format="json"):
    """ Build xml structure with concert metadata

    :param concert_link: (string) link to a concert page
    :param meta_format: (string) data output format: json, xml
    :return: (string xml) concert metadata in xml
    """
    if meta_format not in available_meta_formats:
        return f"{meta_format} is an unknown data format"

    # Set up a concert object
    concert = get_concert_object(concert_link)

    if meta_format == "json":
        return concert.to_json()
    elif meta_format == "xml":
        return concert.to_xml()


def get_concert_object(concert_link):
    """ Build a new concert object and scrape concert event meta from provided event web-page

    :param concert_link: (string) link to an event web-page
    :return: (Concert) concert object with event metadata scanned from web-page
    """
    # Set up concert object
    concert = Concert()
    concert.set_event_link(concert_link)

    # Prepare concert page soup
    page_request = requests.get(concert_link)
    page_soup = BeautifulSoup(page_request.text, 'lxml')

    # Parse concert page
    concert.parse_page_soup(page_soup)

    return concert

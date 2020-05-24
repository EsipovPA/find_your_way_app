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


def get_widget_content(page_soup):
    """ Need to find a way to get pages object automatically.

    :param page_soup: (bs4 object) concert schedule list page
    :return: (string list) object containing pages links
    """
    return page_soup.select(".OW6DD")       # Look at website and check if does not work


def get_concert_list():
    """ Gets list of concerts for afisha moscow website

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
            print(f"page counter = {page_counter}")
            if len(list_items) != 0:
                links_list = []
                for item in list_items:
                    link = item.findAll('a', href=True)
                    if len(link) != 0:
                        concert_list.append(link[0]['href'])

    return concert_list

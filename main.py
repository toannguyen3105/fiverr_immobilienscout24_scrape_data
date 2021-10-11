#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

from models.cookie import CookieModel
from models.store import StoreModel
from models.item import ItemModel

from utils.headers import prepare_headers
from utils.telegram.send_message import send_message_telegram, generate_message
from utils.date_format import getTimeStamp

BASE_URL = "https://www.immobilienscout24.de"


def update_latest_product():
    print("I'm working...")

    cookie_item = CookieModel.find_by_id(1)
    headers = prepare_headers(cookie_item.cookie)

    stores = [store.json() for store in StoreModel.find_all()]
    for store in stores:
        print("I'm in stores loop...")

        req = requests.get(store["url"], headers=headers)
        soup = BeautifulSoup(req.text, "lxml")

        # Absolute link of saved items
        absolute_link_saved_items = [item.json()["absolute_link"] for item in ItemModel.find_all()]

        items = soup.find_all("li", {"class": "result-list__listing"})
        for item in items:
            name = item.find('h5', {"class": "result-list-entry__brand-title"}).text
            price = item.find('dd', {"class": "font-highlight font-tabular"}).text
            absolute_link = get_absolution_link(item)
            store_id = store["id"]
            description = store["description"]

            if absolute_link not in absolute_link_saved_items:
                send_message_telegram(generate_message(name, price, absolute_link, description))

            if ItemModel.find_by_absolute_link(absolute_link, store_id):
                continue
            item = ItemModel(name, price, absolute_link, store_id, getTimeStamp(), None, None, None)
            item.save_to_db()


def get_absolution_link(item):
    link = item.find('a', {"class": "result-list-entry__brand-title-container"})
    return f"{BASE_URL}{link['href']}"

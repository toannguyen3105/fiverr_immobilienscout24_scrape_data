#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from decouple import config

from utils.date_format import get_date_telegram
from utils.emoji import get_random_emoji

TELEGRAM_GROUP_PRICE_FIT_ID = config('TELEGRAM_GROUP_PRICE_FIT_ID')
TELEGRAM_TOKEN_BOT = config('TELEGRAM_TOKEN_BOT')

api_url_telegram = f"https://api.telegram.org/bot{TELEGRAM_TOKEN_BOT}/sendMessage?chat_id=@__groupid__&text="


def send_message_telegram(message):
    final_telegram_url = api_url_telegram.replace("__groupid__", TELEGRAM_GROUP_PRICE_FIT_ID)
    final_telegram_url = final_telegram_url + message
    requests.get(final_telegram_url)


def generate_message(name, price, link, description):
    return f"{get_random_emoji()} " \
           f"Immobilienscout24 24/7  \n" \
           f"**********************  \n" \
           f"**********************  \n" \
           f"Query time: {get_date_telegram()}\n" \
           f"Description: {description}\n" \
           f"Item name: {name}\n" \
           f"Item price: {price}\n" \
           f"Item link: {link}\n"

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import schedule
import time
import logging
import requests
from bs4 import BeautifulSoup

from utils.telegram.send_message import send_message_telegram, generate_message

log_format = '[%(levelname)s] - %(message)s'
logging.basicConfig(level='INFO', format=log_format)


def request_list_company(page):
    company_url_list = []
    logging.info("getting list of company in page " + str(page))
    response = requests.get(page).text
    soup = BeautifulSoup(response, 'html.parser')
    list_of_company_div = soup.find_all("li", class_="result-list__listing ")
    for company_div in list_of_company_div:
        if company_div.find('a')['href']: company_url_list.append(company_div.find('a')['href'])
    logging.info('Get total ' + str(len(company_url_list)) + ' company url')
    return company_url_list


def job():
    page = "https://www.immobilienscout24.de/Suche/radius/wohnung-mieten?centerofsearchaddress=Berlin%3B%3B%3B1276003001%3BBerlin%3B&pricetype=rentpermonth&geocoordinates=52.51051%3B13.43068%3B20.0&sorting=2&enteredFrom=result_list#/"
    print("I'm working...")
    # send_message_telegram(generate_message("I'm working..."))

    company_url_list = request_list_company(page)
    for company_url in company_url_list:
        # get_company_details(company_url)
        pass

    logging.info('Get information of total ' + str(len([])) + ' companies')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    schedule.every(5).seconds.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

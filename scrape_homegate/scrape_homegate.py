#!/usr/bin/env python3

import sys
import os
import requests
import time
import re
import json
from numpy.random import exponential
from bs4 import BeautifulSoup

RESULTS_DIR = 'html/'

UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:63.0) Gecko/20100101 Firefox/63.0'
API_ENDPOINT = '/mieten/immobilien/ort-lausanne/trefferliste'

total_pages = 20

def request(base_url, endpoint, params):
    return requests.get(
        url = base_url + endpoint,
        headers = {
            'User-Agent': UA,
            'Accept': 'text/html',
            'Referer': base_url,
            'Accept-Language': 'de-CH'
        },
        params = params
    )

def get_result_pages(list_html):
    soup = BeautifulSoup(list_html, 'html.parser')

    return [link.get('href') for link in soup.find_all(class_="detail-page-link")]

def download_result_pages(base_url):
    """Download all the rental unit results and store their HTML pages in a folder."""

    for page_index in range(1, total_pages + 1):
        result = request(
            base_url, API_ENDPOINT,
            params = {
                "ep": str(page_index),
                "tab": "list",
                "o": "sortToplisting-desc"
            }
        )

        if result.status_code != 200:
            print(result.status_code)
            print(result.text)
            raise

        time.sleep(exponential(1))

        for result_index, result_page in enumerate(get_result_pages(result.text)):
            result = request(base_url, result_page, {})

            if result.status_code != 200:
                print(result.status_code)
                print(result.text)
                raise

            filename = "{}{}_{}.html".format(
                RESULTS_DIR, page_index, result_index
            )
            with open(filename, "w") as file:
                file.write(result.text)
                print("Written : ", filename)

            time.sleep(exponential(1))

def contains_digits(string):
    return any(char.isdigit() for char in string)

def parse_result_pages():
    rent_units = []

    for result_filename in os.listdir(RESULTS_DIR):
        with open(RESULTS_DIR + result_filename, "r") as file:
            html = file.read()

        soup = BeautifulSoup(html, 'html.parser')
        rent_unit = {}

        address = soup.find(class_="detail-address-link")

        if address.h2 is None:
            rent_unit["address"] = ""
            rent_unit["street"] = ""
        else:
            address_parts = address.h2.string.split(" ")

            rent_unit["address"] = address.h2.string
            rent_unit["street"] = " ".join([
                part for part in address_parts if not contains_digits(part)
            ])
            rent_unit["number"] = " ".join([
                part for part in address_parts if contains_digits(part)
            ])

        city = address.span.string
        rent_unit["postCode"] = city.split(" ")[0]
        rent_unit["city"]= city.split(" ")[1]

        price_string = soup.find(itemprop="price").string
        rent_unit["price"] = re.sub("\D+", "", price_string)

        surface_span = soup.find("span", string="Wohnfläche")

        if surface_span is not None:
            rent_unit["surface"] = surface_span.find_next_sibling("span").span.string
        else:
            rent_unit["surface"] = ""

        rooms_span = soup.find("span", string="Zimmer")

        if rooms_span is None:
            rent_unit["numberRooms"] = ""
        else:
            rent_unit["numberRooms"] = rooms_span.find_next_sibling("span").string

        rent_unit["title"] = soup.find(class_="title").string

        rent_units.append(rent_unit)

    with open('homegate.json', 'w', encoding='utf8') as outfile:
        outfile.write(json.dumps(rent_units, ensure_ascii=False, indent=4))


if __name__ == '__main__':
    if len(sys.argv) != 3 or sys.argv[2] not in ["download", "parse"]:
        print('usage:', sys.argv[0],
              'base_url stage')
        sys.exit(1)
    elif sys.argv[2] == "download":
        download_result_pages(sys.argv[1])
    elif sys.argv[2] == "parse":
        parse_result_pages()

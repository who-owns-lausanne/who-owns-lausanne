import bs4
import json
import os
import re

DATA_DIR = 'data/anibis/offers/'
offer_dicts = []
for i, offer_file in enumerate(os.listdir(DATA_DIR)):
    with open(DATA_DIR + offer_file) as html:


        text = html.read()
        html.seek(0)

        try:
            meublé = 'meublé' in text
            soup = bs4.BeautifulSoup(html, features='lxml')
            price = soup.find('meta', itemprop='price')['content']
            address = soup.find('meta', itemprop = 'streetAddress')['content']
            city = soup.find('meta', itemprop = 'addressLocality')['content']
            zip_num = re.search(r"kvlisting_zip: '(\d+)'", text).group(1)
            rooms = re.search(r"kvnumberOfRooms: '([\d\.]+)'", text).group(1)
            surface = re.search(r"kvlivingSpace: '([\d\.]+)", text).group(1)
        except:
            #skip misbehaving offers
            continue

        res = {
                'meuble':meublé,
                'price':price,
                'address':address,
                'city':city,
                'postCode':zip_num,
                'surface': surface,
                'numberRooms':rooms
        }
        offer_dicts.append(res)

print(json.dumps(offer_dicts))


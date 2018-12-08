import requests
import json
import math
import numpy as np

RAW_DIR = '../../data/raw/tutti/'


def getTutti(page, limit=100):
    cookies = {
        'ajs_user_id': 'null',
        'ajs_group_id': 'null',
        'lang': 'fr',
        'ajs_anonymous_id': '%22bf0a3c34-c83f-4764-a48f-c783309a9f4c%22',
        '_gcl_au': '1.1.253718592.1542968730',
        '_ga': 'GA1.2.1357180133.1542968730',
        '_gid': 'GA1.2.2109516043.1542968730',
        'adw': '12a92c4c-f201-44a3-a5ce-26dbbce57a94',
        '_gat_UA-88671020-1': '1',
    }
    headers = {
        'AlexaToolbar-ALX_NS_PH': 'AlexaToolbar/alx-4.0.3',
        'Origin': 'https://www.tutti.ch',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'fr',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://www.tutti.ch/fr/li/vaud/lausanne/immobilier/appartements?o=2',
        'Connection': 'keep-alive',
        'X-Tutti-Hash': '81fd68a0-47a0-4b8b-9401-4c63cb416c5e',
        'X-Tutti-Source': 'web LIVE-181123-163',
        'DNT': '1',
    }
    params = (
        ('category', '1000'),
        ('limit', limit),
        ('m', '131'),
        ('o', page),
        ('region', '20'),  # Region 20: lausanne
        ('subcategory', ''),
        ('with_all_regions', 'false'),
    )

    response = requests.get('https://api.tutti.ch/v10/list.json',
                            headers=headers, params=params, cookies=cookies)
    return json.loads(response.content)


def saveJson(data, filename):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)


if __name__ == "__main__":
    # Compute number of pages to iterate
    limit = 100
    total_ads = getTutti(page=1, limit=limit)['search_total']
    pages = math.ceil(total_ads / limit)

    # Iterate through all pages in region=20 (Lausanne) and save data locally
    for page in np.arange(1, pages + 1):
        j = getTutti(page=page, limit=limit)
        filename = RAW_DIR + 'page_' + str(page) + '.json'
        print("Scrape and save: ", filename)
        saveJson(j, filename)

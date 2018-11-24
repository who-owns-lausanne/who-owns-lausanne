import requests
import time
import numpy

BASE_URL = 'https://www.anibis.ch'

DATA_DIR = 'data/anibis/'

with open(DATA_DIR + 'listing_urls.txt') as f:
    for i, line in enumerate(f.readlines()):
        r = requests.get(BASE_URL + line.strip())
        if r.status_code != 200:
            raise
        with open(DATA_DIR + 'offers/offer_{}.html'.format(i), 'w') as fw:
            fw.write(r.text)
        print(i, len(r.text))
        #wait 1 second on avg, finish in 17 minutes
        time.sleep(numpy.random.exponential(1))

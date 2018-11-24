URL = 'https://www.anibis.ch/fr/immobilier-immobilier-locations-vaud--434/advertlist.aspx?loc=lausanne&aidl=15222&dlf=1&pi={}'

import requests
import time
import numpy

for pi in range(1, 55):
    r = requests.get(URL.format(pi))
    if r.status_code == 200:
        with open('data/anibis/listings_{}.html'.format(pi), 'w') as f:
            f.write(r.text)
    else:
        raise

    print(pi)
    time.sleep(numpy.random.exponential(1))

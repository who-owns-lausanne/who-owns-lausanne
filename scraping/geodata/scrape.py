import os, sys
import requests
import time
from numpy import linspace
from numpy.random import exponential

RESULTS_DIR = 'scraped/'

UA = 'Mozilla/5.0 (X11; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0'
API_ENDPOINT = '/prod/wsgi/mapserv_proxy'

total_wait = 15*60 #how many seconds we are willing to wait

query_string = r"""<?xml version="1.0"?>
<wfs:GetFeature xmlns:wfs="http://www.opengis.net/wfs" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" service="WFS" version="1.1.0" maxFeatures="200" xsi:schemaLocation="http://www.opengis.net/wfs http://schemas.opengis.net/wfs/1.1.0/wfs.xsd">
  <wfs:Query xmlns:feature="http://mapserver.gis.umn.edu/mapserver" typeName="feature:bdcad_bf_parc_pol">
    <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
      <ogc:BBOX>
        <ogc:PropertyName>geom</ogc:PropertyName>
        <gml:Envelope xmlns:gml="http://www.opengis.net/gml">
          <gml:lowerCorner>{lowerWest} {lowerNorth}</gml:lowerCorner>
          <gml:upperCorner>{upperWest} {upperNorth}</gml:upperCorner>
        </gml:Envelope>
      </ogc:BBOX>
    </ogc:Filter>
  </wfs:Query>
</wfs:GetFeature>
"""

if len(sys.argv) != 6:
    print('usage:', sys.argv[0],
          'base_url topLeftWest topLeftNorth bottomRightWest bottomRightNorth')
    sys.exit(1)

BASE_URL = sys.argv[1]
upperWest, upperNorth, lowerWest, lowerNorth =\
        (float(arg) for arg in sys.argv[2:])

n_grid_x = 20
width_x = (lowerWest - upperWest)/n_grid_x
n_grid_y = 20
width_y = (upperNorth - lowerNorth)/n_grid_x


def coord_to_filename(uW, uN, lW, lN):
    return RESULTS_DIR + '_'.join(
            str(fl) for fl in [uW, uN, lW, lN]
            ) + '.xml'

def is_saved(uW, uN, lW, lN):
    return os.path.isfile(coord_to_filename(uW, uN, lW, lN))

def query(uW, uN, lW, lN):
        q = query_string.format(
                    lowerWest = lW,
                    lowerNorth = lN,
                    upperWest = uW,
                    upperNorth = uN
                )

        r = requests.request(
            'POST',
            BASE_URL + API_ENDPOINT,
            data = q,
            headers = {
                'User-Agent': UA,
                'Accept': '*/*',
                'Referer': BASE_URL,
                'Content-Type': 'application/xml'
                }
        )
        return r

for uN in linspace(upperNorth, lowerNorth, n_grid_y):
    for uW in linspace(upperWest, lowerWest, n_grid_x):
        lW = uW + width_x
        lN = uN - width_y

        bbox = uW, uN, lW, lN

        #skip query if file already exists
        if is_saved(*bbox):
            print('skipping')
            continue

        # sleep for a random amount of time
        # the sleep time is an exponential rv
        wait_time = exponential(total_wait / (n_grid_x * n_grid_y))
        print('wait:', wait_time)
        time.sleep(wait_time)
        res = query(*bbox)
        if res.status_code != 200:
            print(res.status_code)
            print(res.text)
            raise

        with open(coord_to_filename(*bbox), 'w') as fw:
            fw.write(res.text)

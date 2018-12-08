import json
import re


DATA_DIR = 'data/raw/maps/'

ad_bats = json.load(open(DATA_DIR + 'addresses_batiments.geojson'))
# Discard addresses with RUE_ABR == None, there's about 500 of them out of 63K
batiments = [bat for bat in ad_bats['features']
             if bat['properties']['RUE_ABR']]

regex_cache = {}


def to_num(number):
    "extract a numerical prefix out of the string (9B becomes 9)"
    i = 0
    while number[:i + 1].isdecimal() and i < len(number):
        i += 1
    return number[:i]


def street_match(rue_abr, street):
    if rue_abr in regex_cache:
        regex = regex_cache[rue_abr]
    else:
        pattern = rue_abr.lower().replace('.', '(\.)?').replace('-', '[- ]')
        regex = re.compile(r'\b' + pattern + r'\b', flags=re.IGNORECASE)
        regex_cache[rue_abr] = regex
    return regex.search(street)


def address_to_coords(street, number):
    number = to_num(number)
    for building in batiments:
        rue_abr = building['properties']['RUE_ABR']
        if street_match(rue_abr, street) and\
                building['properties']['TEXTSTRING'] == number:
            # only match when street number and street coincide
            return building['geometry']['coordinates'], rue_abr
    # Else return None if no match
    return None


def main(offers):
    """returns a list of offers with position resolved. offers not
    matchin any position are dropped"""
    res = []
    for offer in offers:
        coords_rue = address_to_coords(offer['street'], offer['number'])
        if coords_rue:
            coords, rue_abr = coords_rue
            offer['position'] = coords
            res.append(offer)

    return res

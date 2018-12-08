import json
import re


"""
Take N json files of addresses as argument and returns a single one with
invalid entries removed duplicates removed and street names standardized (Av.
-> Avenue, Ch. -> Chemin, etc)
"""


def valid(offer):
    """an offer is valid if it is clean and usable"""

    address_valid = offer['address'] != ''

    try:
        price = float(offer['price'])  # throws if fails
        price_valid = price > 0.
    except:
        price_valid = False

    try:
        surface = int(offer['surface'])
        surface_valid = surface > 10
    except:
        surface_valid = False

    return address_valid and surface_valid and price_valid


def standardize_address(offer):
    """use the address format used in the address cadastral layer"""
    replacements = {
        r'\bav\.|\bavenue\b': 'av',
        r'\broute\b': 'rte',
        r'\bruelle\b': 'rlle',
        r'prom\.|\bpromenade\b': 'prom',
        r'\bpl\.|\bplace\b': 'pl',
        r'\bpass\.|\bpassage\b': 'pass',
        r'\bch\.|\bchemin\b': 'ch',
        r'\bboulevard\b': 'bd',
    }
    street = offer['street']
    for pattern in replacements:
        street = re.sub(pattern, replacements[pattern], street,
                        flags=re.IGNORECASE)

    res = offer.copy()
    res['street'] = street

    return res


def offers_equal(o1, o2):
    return (o1['address'] == o2['address']) and\
        (float(o1['price']) == float(o2['price']))


def main(filenames):
    all_files = []
    for filename in filenames:
        all_files = all_files + json.load(open(filename))

    offers = sorted(
        [standardize_address(off) for off in all_files
         if valid(off)],
        key=lambda o: (o['address'], float(o['price']))
    )

    prev = offers[0]
    dedupes = [prev]

    for cur in offers[1:]:
        if not offers_equal(cur, prev):
            dedupes.append(cur)
        prev = cur

    return dedupes

import json
import re
import sys

"""
Take 2 json files of addresses as argument and returns a single one with
invalid entries removed duplicates removed and street names standardized (Av.
-> Avenue, Ch. -> Chemin, etc)
"""

def valid(offer):
    try:
        # if conversion fails, return false because price is not numerical
        float(offer['price'])
    except:
        return False
    return offer['surface'].isdecimal() and offer['address'] != '' and\
            int(offer['surface']) != 0 and float(offer['price']) != 0.

def standardize_address(offer):
    replacements = {
            r'\bavenue\b':'av',
            r'\broute\b':'rte',
            r'\bruelle\b':'rlle',
            r'\bpromenade\b':'prom',
            r'\bplace\b':'pl',
            r'\bpassage\b':'pass',
            r'\bchemin\b':'ch',
            r'\bboulevard\b':'bd',
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


if __name__ == '__main__':

    addresses_1 = json.load(open(sys.argv[1]))
    addresses_2 = json.load(open(sys.argv[2]))

    addresses = sorted(
            [standardize_address(add) for add in (addresses_1 + addresses_2)
                if valid(add)],
            key=lambda o: o['address']
            )

    prev = addresses[0]
    dedupes = [prev]

    for cur in addresses[1:]:
        if not offers_equal(cur, prev):
            dedupes.append(cur)
        prev = cur

    print(json.dumps(dedupes, ensure_ascii=False, indent=2))

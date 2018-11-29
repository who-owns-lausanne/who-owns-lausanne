import sys
import json


def is_streetnumber(word):
    "True if word starts with a digit"
    return word.startswith(
        tuple(
            str(num) for num in range(10)
        )
    )


offers_filename = sys.argv[1]
result = []
with open(offers_filename) as f:
    offers = json.load(f)
    for offer in offers:
        street = ' '.join([word
                           for word in offer['address'].split()
                           if not is_streetnumber(word)])
        number = ' '.join([number
                           for number in offer['address'].split()
                           if is_streetnumber(number)])

        offer['street'] = street
        offer['number'] = number
        result.append(offer)

print(json.dumps(result, indent=2, ensure_ascii=False))

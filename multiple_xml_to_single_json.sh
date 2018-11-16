#! /bin/bash

# we first access the attribute objects, we then rewrap this objects
# in simples json objects with cleaner field names. Finally we concatenate
# all the objects in a single list.

XQ_SCRIPT=\
'.["wfs:FeatureCollection"]["gml:featureMember"][]["ms:bdcad_bf_parc_pol"]'\
'| {"numcom":.["ms:numcom"], "no_parc":.["ms:no_parc"],'\
'"proprio":.["ms:proprio"]}'

xq "$XQ_SCRIPT" scraped/* | jq --slurp >proprio.json

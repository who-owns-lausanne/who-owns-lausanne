#! /bin/bash

# we first access the attribute objects, we then rewrap this objects
# in simples json objects with cleaner field names. Finally we concatenate
# all the objects in a single list.

# $1 argument represent the output file name,
# if not assigned, set default.
if [ -z "$1" ]
then
      name="all_owners_dirty.json"
else
      name=$1
fi

XQ_SCRIPT=\
'.["wfs:FeatureCollection"]["gml:featureMember"][]["ms:bdcad_bf_parc_pol"]'\
'| {"numcom":.["ms:numcom"], "no_parc":.["ms:no_parc"],'\
'"proprio":.["ms:proprio"]}'

xq "$XQ_SCRIPT" ./data/raw/owners/* | jq --slurp '.' > ./data/owners/$name
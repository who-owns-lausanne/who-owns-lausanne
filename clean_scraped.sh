#! /bin/bash
 xq '.["wfs:FeatureCollection"]["gml:featureMember"][]["ms:bdcad_bf_parc_pol"] | {"numcom":.["ms:numcom"], "no_parc":.["ms:no_parc"], "proprio":.["ms:proprio"]}' scraped/* | jq --slurp >proprio.json

# FOLIUM TOOLS

import folium
import numpy as np
from matplotlib import colors, cm
import branca.colormap as cmb


def getMap():
    return folium.Map([46.524, 6.63], tiles="cartodbpositron", zoom_start=14)


def add_marker(map_, lat, long, price, min_price, max_price):
    color_rgb = cm.RdYlGn(1.0 - (price - min_price) / (max_price - min_price))
    color_hex = colors.to_hex(color_rgb, keep_alpha=False)

    # Marker wants first the N coordinate and then E
    folium.CircleMarker(
        (lat, long),
        radius=5,
        fill_color=color_hex,
        weight=0,
        fill_opacity=0.8,
        tooltip=price,
    ).add_to(map_)


def heatmap_prices_from_json(rent_prices):
    """Given JSON file with position and price, return heatmap with prices"""

    min_price, max_price = np.quantile(
        [offer["CHF/m2"] for offer in rent_prices], q=(0.05, 0.90)
    )

    m = getMap()
    for offer in rent_prices:
        add_marker(
            m,
            offer["position"][1],
            offer["position"][0],
            offer["CHF/m2"],
            min_price,
            max_price,
        )
    return m


def heatmap_prices_per_parcels(geo_parcels, rent_prices):
    """Given pandas dataframe with position and price, return heatmap with prices"""
    map = getMap()

    rent_prices = rent_prices.set_index("parc_no")

    min_price, max_price = np.quantile(rent_prices["price"], q=(0.05, 0.90))
    colormap = cmb.linear.RdYlGn_06.scale(min_price, max_price)

    # invert colors
    colormap.colors = colormap.colors[::-1]
    colormap.caption = "Rent prices in CHF/m2"

    def style_function(feature):
        parcel_id = feature["properties"]["NO_PARC"]
        price = rent_prices.loc[parcel_id]["price"]

        return {"stroke": False, "fillColor": colormap(price), "fillOpacity": 0.75}

    folium.GeoJson(geo_parcels, style_function=style_function).add_to(map)
    map.add_child(colormap)

    return map

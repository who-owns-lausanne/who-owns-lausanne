# FOLIUM TOOLS

import folium
import numpy as np
import matplotlib.cm as cm
import matplotlib.colors as colors


def getMap():
    return folium.Map([46.524, 6.63], tiles='cartodbpositron', zoom_start=14)


def heatmap_prices_from_json(rent_prices):
    """Given JSON file with position and price, return heatmap with prices"""

    min_price, max_price = np.quantile(
        [offer['CHF/m2'] for offer in rent_prices], q=(0.05, 0.90))

    m = getMap()
    for offer in rent_prices:
        coords = offer['position']

        color_rgb = cm.RdYlGn(
            1. - (offer['CHF/m2'] - min_price) / (max_price - min_price))
        color_hex = colors.to_hex(color_rgb, keep_alpha=False)

        # Marker wants first the N coordinate and then E
        folium.CircleMarker(
            (coords[1], coords[0]),
            radius=5, fill_color=color_hex, weight=0, fill_opacity=0.8, tooltip=offer['CHF/m2']
        ).add_to(m)
    return m


def heatmap_prices_from_pd(rent_prices):
    """Given pandas dataframe with position and price, return heatmap with prices"""
    map_ = getMap()

    def add_maker(map_, coords, price, min_price, max_price):
        color_rgb = cm.RdYlGn(
            1. - (price - min_price) / (max_price - min_price))
        color_hex = colors.to_hex(color_rgb, keep_alpha=False)

        # Marker wants first the N coordinate and then E
        folium.CircleMarker(
            (coords[1], coords[0]),
            radius=5, fill_color=color_hex, weight=0, fill_opacity=0.8, tooltip=price
        ).add_to(map_)

    min_price, max_price = np.quantile(rent_prices['price'], q=(0.05, 0.90))
    _ = rent_prices.apply(lambda row: add_maker(
        map_, row['position'], row['price'], min_price, max_price), axis='columns')
    return map_

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


def heatmap_prices(rent_prices):
    """Given JSON file with position and price, return heatmap with prices"""

    min_price, max_price = np.quantile(rent_prices['CHF/m2'], q=(0.05, 0.90))

    m = folium.Map([46.524, 6.63], tiles="cartodbpositron", zoom_start=14)

    rent_prices.apply(lambda r: add_marker(
        m, r['lat'], r['long'], r['CHF/m2'], min_price, max_price), axis='columns')

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


def heatmap_nan(map_data):
    """Given JSON file with position and price, return heatmap with prices"""

    map = getMap()

    def style_function(feature):
        """Returns color red for missing values, blue for valid."""

        # feature in this cas is not a geopandas object, rather a
        # geoJson where np.nan are None
        return {
            'fillColor':
            'red' if feature['properties']['owner'] is None else 'blue',
            'stroke': False
        }

    geo_fol = folium.GeoJson(
        map_data, style_function=style_function)

    map.add_child(geo_fol)
    return map


def heatmap_category(parcelles, owners_categories):
    m = getMap()

    def style_function(feature):
        colors = {
            'coop': 'yellow',
            'société': 'red',
            'public': 'green',
            'private': 'blue',
            'PPE': 'orange',
            'pension': 'purple',
            'fondation/association': 'brown'

        }
        owner = feature['properties']['owner']
        cat = owners_categories.loc[owner][0]

        return {
            'stroke': False,
            'fillColor': colors[cat]
        }

    folium.GeoJson(
        parcelles,
        style_function=style_function,
        # show the owner at hover
        tooltip=folium.GeoJsonTooltip(['owner'])
    ).add_to(m)

    return m


def heatmap_all_rents(rents, quartiers):
    """draw a map showing the location of each vacancy, and the quartiers borders"""

    def add_maker(m, position, chf_m2):
        lat = position[1]
        long = position[0]
        folium.Marker((lat, long), tooltip=chf_m2).add_to(m)

    m = getMap()
    folium.GeoJson(quartiers).add_to(m)
    rents.apply(lambda row:
                add_maker(m, row['position'], row['CHF/m2']), axis='columns')
    return m


def heatmap_all_rents_by_quartiers(rents, quartiers):

    def add_maker(m, position, quartier):
        lat = position[1]
        long = position[0]

        color = '%06x' % (hash(quartier) % (256**3))

        folium.CircleMarker((lat, long),
                            radius=5,
                            fill_color='#' + color,
                            weight=0,
                            fill_opacity=1
                            ).add_to(m)
    m = getMap()
    folium.GeoJson(quartiers).add_to(m)

    rents.apply(lambda row: add_maker(
        m, row['position'], row['quartier']), axis='columns')

    return m

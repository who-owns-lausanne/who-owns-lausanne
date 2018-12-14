# FOLIUM TOOLS

import folium
import numpy as np
from matplotlib import colors, cm
import branca.colormap as cmb


def getMap():
    return folium.Map([46.524, 6.63], tiles="cartodbpositron", zoom_start=14)


def missing_values(geodata):  # USED
    """Given geoJSON file, return a map that show missing values."""

    m = getMap()

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
        geodata, style_function=style_function)

    m.add_child(geo_fol)
    return m


def by_owners_category(parcelles, owners_categories):  # USED
    """Return a map where different categories parcelles have different colors."""
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


def marker_rents_with_quartiers(rents, quartiers):  # USED
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


def circles_rents(rents, quartiers):  # USED
    """Return a map where rents in the same quartiers have same colors"""
    def add_circle(m, position, quartier):
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

    rents.apply(lambda row: add_circle(
        m, row['position'], row['quartier']), axis='columns')

    return m


def circles_prices(rent_prices):  # USED
    """Return map with different circles color for different rent price"""
    min_price, max_price = np.quantile(rent_prices['CHF/m2'], q=(0.05, 0.90))
    m = folium.Map([46.524, 6.63], tiles="cartodbpositron", zoom_start=14)

    def add_circle(map_, lat, long, price, min_price, max_price):
        color_rgb = cm.RdYlGn(
            1.0 - (price - min_price) / (max_price - min_price))
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

    rent_prices.apply(lambda r: add_circle(
        m, r['lat'], r['long'], r['CHF/m2'], min_price, max_price), axis='columns')
    return m


def parcelles_prices(prices):  # USED
    """Return a heatmap where different parcelle prices have different colors"""
    m = getMap()

    rent_prices = prices.set_index("parc_num")

    min_price, max_price = np.quantile(rent_prices["CHF/m2"], q=(0.05, 0.90))
    colormap = cmb.linear.RdYlGn_06.scale(min_price, max_price)

    # invert colors
    colormap.colors = colormap.colors[::-1]
    colormap.caption = "Rent prices in CHF/m2"

    def style_function(feature):
        return {"stroke": False, "fillColor": colormap(feature['properties']['CHF/m2']), "fillOpacity": 0.75}

    folium.GeoJson(prices._to_geo(), style_function=style_function).add_to(m)
    m.add_child(colormap)

    return m


def parcelles_prices_by_quartiers(parcelles):  # USED
    """Return heatmap of parcelles prices by quartiers"""

    def style_function_quartiers(feature):

        min_price, max_price = np.quantile(parcelles["CHF/m2"], q=(0.05, 0.90))

        colormap = cmb.linear.RdYlGn_06.scale(min_price, max_price)

        # invert colors
        colormap.colors = colormap.colors[::-1]
        colormap.caption = "Rent price by quartiers"

        quartier_name = feature['properties']['Name']
        if (quartier_name == '90 - Zones foraines'):
            price = 0
        else:
            price = parcelles[parcelles['Name'] ==
                              quartier_name]['CHF/m2'].values[0]

        return {"stroke": False, "fillColor": colormap(price), "fillOpacity": 0.75}

    m = getMap()
    folium.GeoJson(parcelles._to_geo(),
                   style_function=style_function_quartiers,
                   tooltip=folium.GeoJsonTooltip(['CHF/m2', 'Name'])
                   ).add_to(m)
    return m

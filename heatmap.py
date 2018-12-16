# FOLIUM TOOLS

import folium
import numpy as np
from matplotlib import colors, cm
import branca.colormap as cmb

OWNERSHIP_COLORS = {
    'coop': 'yellow',
    'société': 'red',
    'public': 'green',
    'private': 'blue',
    'PPE': 'orange',
    'pension': 'purple',
    'fondation/association': 'brown'
}

OPACITY = 0.75


def getMap(tiles="cartodbpositron"):
    return folium.Map([46.524, 6.63], tiles=tiles, zoom_start=14)


def missing_values(geodata):
    """Given geoJSON file, return a map that show missing values."""

    m = getMap()

    def style_function(feature):
        """Returns color red for missing values, blue for valid."""

        # feature in this case is not a geopandas object, rather a
        # geoJson where np.nan are None
        return {
            "fillColor": "red" if feature["properties"]["owner"] is None else "blue",
            "stroke": False,
        }

    geo_fol = folium.GeoJson(geodata, style_function=style_function)
    m.add_child(geo_fol)
    return m


def by_owners_category(parcelles, parcelles_categories):
    """Return a map where different categories parcelles have different colors."""
    m = getMap()

    def style_function(feature):
        parc_num = feature["properties"]["parc_num"]
        cat = parcelles_categories.loc[parc_num][0]

        return {
            "stroke": False,
            "fillColor": OWNERSHIP_COLORS[cat],
        }

    folium.GeoJson(
        parcelles,
        style_function=style_function,
    ).add_to(m)
    return m


def marker_rents_with_quartiers(rents, quartiers):
    """draw a map showing the location of each vacancy, and the quartiers borders"""

    def add_marker(m, position, chf_m2):
        lat = position[1]
        long = position[0]
        folium.Marker((lat, long), tooltip=chf_m2).add_to(m)

    m = getMap()
    folium.GeoJson(quartiers).add_to(m)
    rents.apply(
        lambda row: add_marker(m, row["position"], row["CHF/m2"]), axis="columns"
    )
    return m


def circles_rents(rents, quartiers):
    """Return a map where rents in the same quartiers have same colors"""

    def add_circle(m, position, quartier):
        lat = position[1]
        long = position[0]

        color = "%06x" % (hash(quartier) % (256 ** 3))

        folium.CircleMarker(
            (lat, long), radius=5, fill_color="#" + color, weight=0, fill_opacity=1
        ).add_to(m)

    m = getMap()
    folium.GeoJson(quartiers).add_to(m)

    rents.apply(
        lambda row: add_circle(m, row["position"], row["quartier"]), axis="columns"
    )
    return m


def rent_price_colormap(prices, title):
    min_price, max_price = np.quantile(prices, q=(0.05, 0.90))
    colormap = cmb.linear.RdYlGn_06.scale(min_price, max_price)

    # invert colors
    colormap.colors = colormap.colors[::-1]
    colormap.caption = title
    return colormap


def __circles_prices(layer, rent_prices):
    colormap = rent_price_colormap(
        rent_prices["CHF/m2"], "Listed offers with prices in CHF/m^2"
    )

    def add_circle(m, lat, long, price):
        # Marker wants first the N coordinate and then E
        folium.CircleMarker(
            (lat, long),
            radius=5,
            fill_color=colormap(price),
            weight=0,
            tooltip=price,
            fill_opacity=1,
        ).add_to(m)

    rent_prices.apply(
        lambda r: add_circle(layer, r["lat"], r["long"], r["CHF/m2"]), axis="columns"
    )
    return colormap


def circles_prices(rent_prices):
    """Return map with different circles color for different rent price"""
    m = getMap()
    colormap = __circles_prices(m, rent_prices)
    m.add_child(colormap)
    return m


def __parcelles_prices(layer, prices):
    colormap = rent_price_colormap(
        prices["CHF/m2"], "rent prices in CHF/m2""
    )

    def style_function(feature):
        price = feature["properties"]["CHF/m2"]
        return {
            "stroke": False,
            "fillColor": colormap(price),
            "fillOpacity": OPACITY
        }

    folium.GeoJson(
        prices._to_geo(),
        style_function=style_function,
        tooltip=folium.GeoJsonTooltip(["CHF/m2"]),
    ).add_to(layer)

    return colormap


def parcelles_prices(prices):
    """Return a heatmap where different parcelle prices have different colors"""
    m = getMap()
    colormap = __parcelles_prices(m, prices)
    m.add_child(colormap)

    return m


def __parcelles_prices_by_quartiers(layer, parcelles):

    def style_function_quartiers(feature):
        quartier_name = feature["properties"]["Name"]
        if quartier_name == "90 - Zones foraines":
            price = 0
        else:
            price = parcelles[parcelles["Name"] ==
                              quartier_name]["CHF/m2"].values[0]

        return {
            "stroke": False,
            "fillColor": colormap(price),
            "fillOpacity": OPACITY
        }

    folium.GeoJson(
        parcelles._to_geo(),
        style_function=style_function_quartiers,
        tooltip=folium.GeoJsonTooltip(["Name", "CHF/m2"]),
    ).add_to(layer)

    colormap = rent_price_colormap(
        parcelles["CHF/m2"], "Average rent prices in CHF/m^2"
    )
    return colormap


def parcelles_prices_by_quartiers(parcelles):
    """Return heatmap of parcelles prices by quartiers"""
    m = getMap()
    colormap = __parcelles_prices_by_quartiers(m, parcelles)
    m.add_child(colormap)
    return m


def get_choropleth(parcelles, parcels_categories):
    def style_function(feature):
        parc_num = feature["properties"]["parc_num"]
        cat = parcels_categories.loc[parc_num][0]

        return {
            "stroke": False,
            "fillColor": OWNERSHIP_COLORS[cat],
        }

    return folium.GeoJson(
        parcelles,
        style_function=style_function,
    )


def by_owners_all_in_one(parcelles,
                         parcels_categories,
                         parcels_categories_denoised, tiles=True):
    """Return a map where different categories parcelles have different colors."""

    m = getMap(tiles=None)

    layer1 = folium.map.FeatureGroup(
        name='1. Distribution of owners type',
        overlay=False
    ).add_to(m)
    get_choropleth(
        parcelles, parcels_categories
    ).add_to(layer1)

    if (tiles):
        tile_layer = folium.TileLayer('cartodbpositron')
        tile_layer.add_to(layer1)

    layer2 = folium.map.FeatureGroup(
        name='2. Distribution of owners type denoised',
        overlay=False
    ).add_to(m)

    get_choropleth(
        parcelles, parcels_categories_denoised
    ).add_to(layer2)

    if (tiles):
        tile_layer = folium.TileLayer('cartodbpositron')
        tile_layer.add_to(layer2)

    folium.LayerControl(
        position='bottomright',
        collapsed=False
    ).add_to(m)

    return m


def __test(layerx):
    folium.CircleMarker(
        (46.531976, 6.649698),
        radius=5,
        fill_color='green',
        weight=0,
        tooltip=5,
        fill_opacity=1,
    ).add_to(layerx)


def by_rents_all_in_one(rent_prices, prices_by_quartier, parcelles_prices):
    """Return a map where different categories parcelles have different colors."""

    m = getMap(tiles=None)

    # Layer 1 - Rent prices
    layer1 = folium.map.FeatureGroup(
        name='Rent prices',
        overlay=False
    ).add_to(m)
    colormap = __circles_prices(layer1, rent_prices)
    tile_layer = folium.TileLayer('cartodbpositron')
    tile_layer.add_to(layer1)

    # Layer 2 - Rents per quartier
    layer2 = folium.map.FeatureGroup(
        name='Rent prices by quartier',
        overlay=False
    ).add_to(m)
    colormap = __parcelles_prices_by_quartiers(layer2, prices_by_quartier)
    tile_layer = folium.TileLayer('cartodbpositron')
    tile_layer.add_to(layer2)

    # Layer 3 - All parcelles with prices
    layer3 = folium.map.FeatureGroup(
        name='Prices for each parcelle',
        overlay=False
    ).add_to(m)
    colormap = __parcelles_prices(layer3, parcelles_prices)
    tile_layer = folium.TileLayer('cartodbpositron')
    tile_layer.add_to(layer3)

    m.add_child(colormap) # Does not work
    # Add Legend to switch between layer
    folium.LayerControl(
        position='bottomright',
        collapsed=False
    ).add_to(m)

    return m

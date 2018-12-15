# FOLIUM TOOLS

import folium
import numpy as np
from matplotlib import colors, cm
import branca.colormap as cmb

OWNERSHIP_COLORS = {
    "coop": "#ffffb3",
    "société": "#fb8072",
    "public": "#b3de69",
    "private": "#8dd3c7",
    "PPE": "#fdb462",
    "pension": "#bebada",
    "fondation/association": "#80b1d3",
}

OPACITY = 0.75


def getMap():
    return folium.Map([46.524, 6.63], tiles="cartodbpositron", zoom_start=13)


def missing_values(geodata):  # USED
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


def by_owners_category(parcelles, owners_categories):  # USED
    """Return a map where different categories parcelles have different colors."""
    m = getMap()

    def style_function(feature):
        owner = feature["properties"]["owner"]
        cat = owners_categories.loc[owner][0]

        return {
            "stroke": False,
            "fillColor": OWNERSHIP_COLORS[cat],
            "fillOpacity": OPACITY,
        }

    folium.GeoJson(
        parcelles,
        style_function=style_function,
        # show the owner at hover
        # tooltip=folium.GeoJsonTooltip(["owner"]),
    ).add_to(m)
    return m


def marker_rents_with_quartiers(rents, quartiers):  # USED
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


def circles_rents(rents, quartiers):  # USED
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


def circles_prices(rent_prices):  # USED
    """Return map with different circles color for different rent price"""
    colormap = rent_price_colormap(
        rent_prices["CHF/m2"], "Listed offers with prices in CHF/m^2"
    )

    def add_circle(map_, lat, long, price):
        # Marker wants first the N coordinate and then E
        folium.CircleMarker(
            (lat, long),
            radius=5,
            fill_color=colormap(price),
            weight=0,
            tooltip=price,
            fill_opacity=1,
        ).add_to(map_)

    m = getMap()
    rent_prices.apply(
        lambda r: add_circle(m, r["lat"], r["long"], r["CHF/m2"]), axis="columns"
    )
    m.add_child(colormap)
    return m


def parcelles_prices(prices):  # USED
    """Return a heatmap where different parcelle prices have different colors"""

    rent_prices = prices.set_index("parc_num")
    colormap = rent_price_colormap(
        rent_prices["CHF/m2"], "Extrapolated rent prices in CHF/m^2"
    )

    def style_function(feature):
        price = feature["properties"]["CHF/m2"]
        return {"stroke": False, "fillColor": colormap(price), "fillOpacity": OPACITY}

    m = getMap()
    folium.GeoJson(
        prices._to_geo(),
        style_function=style_function,
        tooltip=folium.GeoJsonTooltip(["CHF/m2"]),
    ).add_to(m)
    m.add_child(colormap)
    return m


def parcelles_prices_by_quartiers(parcelles):  # USED
    """Return heatmap of parcelles prices by quartiers"""

    colormap = rent_price_colormap(
        parcelles["CHF/m2"], "Average rent prices in CHF/m^2"
    )

    def style_function_quartiers(feature):
        quartier_name = feature["properties"]["Name"]
        if quartier_name == "90 - Zones foraines":
            price = 0
        else:
            price = parcelles[parcelles["Name"] == quartier_name]["CHF/m2"].values[0]

        return {"stroke": False, "fillColor": colormap(price), "fillOpacity": OPACITY}

    m = getMap()
    folium.GeoJson(
        parcelles._to_geo(),
        style_function=style_function_quartiers,
        tooltip=folium.GeoJsonTooltip(["Name", "CHF/m2"]),
    ).add_to(m)
    m.add_child(colormap)
    return m

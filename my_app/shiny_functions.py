#!/usr/bin/env/ python
# import packages
import numpy as np
import pandas as pd
import ipyleaflet
from branca.colormap import linear
import matplotlib as mpl
import ipywidgets

# groupby func
def groupby_mult(df, groupby_list, agg_dict, sort_list):
    """
    Pass df, groupby list and agg dict, sort order list
    Will return new df
    """
    df_grouped = df.groupby(groupby_list).agg(agg_dict)\
    .sort_values(by=sort_list,ascending=False).reset_index()
    return df_grouped

# function to create rate per 1k columns
def rate_per_1k(df, col_list, new_col_list, pop="population"):
    """
    Pass df, column list and new column name list to function.
    Will create new rate per 1k population columns for those passed
    """
    df["pop_per_1k"] = round(df[pop] / 1000)
    for (col,new_col) in zip(col_list, new_col_list):
        df[new_col] = round(df[col] / df["pop_per_1k"] * 100,2)
    # format pop cols

# function to convert rgb to hex
def rgb_to_hex(rgb_col_list):
    """
    Pass rgb colors in list and return hex
    """
    col_list = [mpl.colors.to_hex(col) for col in rgb_col_list]
    return col_list


# function to divide metric
def divide_metric(df,colmetric,parts=7):
    """
    Pass df and creates N equal parts from min/max
    Returns list
    """
    min_metric = min(df[colmetric])
    max_metric = max(df[colmetric])
    metric = np.linspace(min_metric,max_metric,parts)
    metric = [round(x,2) for x in metric]
    return metric

# function to generate map
def int_choro_ipyleaflet(geojson_gdf, gdf, value, title, metric, rgb_list,
                         colormap):
    """
    Returns an interactive choropleth ipyleaflet map
    Pass GeoJSON indexed by key in key, value (column you want to express)
    GeoDataframe where you want keys expressed from.
    title = Legend title which acts as map title
    Default colormap is blue
    """
    # map key value dict
    key_value_dict =  dict(zip(gdf.index.tolist(),\
                                   gdf[value].tolist()))

    # label below map
    label = ipywidgets.Label(layout=ipywidgets.Layout(width="100%"))

    # base map
    basemap = ipyleaflet.Map(center = (38, -99), 
                   max_zoom=6,
                   min_zoom=2,
                   zoom_control=True,
                   zoom=4,
                   scroll_wheel_zoom=True,
                   dragging=True)
    # add scale              
    basemap.add_control(ipyleaflet.leaflet.ScaleControl(position="bottomleft"))

    # choropleth object
    choro_layer = ipyleaflet.Choropleth(
        geo_data=geojson_gdf,
        choro_data=key_value_dict,
        colormap=colormap,
        nan_color="grey",
        nan_opacity=0.5,
        border_color='black',
        style={'fillOpacity': 0.8})

    # add to basemap
    basemap.add_layer(choro_layer)

    # add on_hover and on_click info
    hover_click_layer = ipyleaflet.GeoJSON(data=geojson_gdf,
                            style={'color': 'black', 'fillColor': '#3366cc', 'opacity':0.0, 
                                   'weight':1.9, 'dashArray':1, 'fillOpacity':0.0},
                            hover_style={'stroke':True, 'color':'#4B86F7', 'weight':5,
                                   'opacity':0.75, 'dashArray':1},
                            name = 'states')

    # hover callback function
    def hover_handler(event=None, feature=None, id=None, properties=None):
        label.value =\
        f'State: {properties["stusps"]},\
        Population per 1k: {properties["pop_per_1k"]},\
        Mass Shooting per 1k: {properties["count_per_1k"]}'
        
    # click callback function
    def click_handler(event=None, feature=None, id=None, properties=None):
        label.value =\
        f'State: {properties["state"]},\
        Population: {properties["population"]},\
        Gun Laws: {properties["lawtotal"]}\
        Injured per 1k: {properties["injured_per_1k"]},\
        Killed per 1k: {properties["killed_per_1k"]}'

    # add hover and click to layer
    hover_click_layer.on_hover(hover_handler)
    hover_click_layer.on_click(click_handler)

    # add to basemap
    basemap.add_layer(hover_click_layer)

    # add and customize legend
    legend = ipyleaflet.LegendControl({metric[0]:rgb_list[0],
                                      metric[1]:rgb_list[1],
                                      metric[2]:rgb_list[2],
                                      metric[3]:rgb_list[3],
                                      metric[4]:rgb_list[4],
                                      metric[5]:rgb_list[5],
                                      metric[6]:rgb_list[6]}, 
                                      name=title, position="bottomright")
    # add to basemap
    basemap.add_control(legend)

    # display map and label
    return ipywidgets.VBox([basemap, label])

if __name__ == "__main__":
    None
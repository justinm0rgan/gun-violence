#!/usr/bin/env/ python
# import built in modules
import pandas as pd
import numpy as np
import geopandas as gpd
import os
import pickle
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import folium
import calendar

# set directory
PROJECT_DIR = os.path.dirname("..")
IMAGES_PATH = os.path.join(PROJECT_DIR, 'images')
os.makedirs(IMAGES_PATH, exist_ok=True)

# functions start here
# function for saving figures
def save_fig(fig_id, tight_layout=True, fig_extension="png", resolution=250, transparent=False):
    '''Function that saves visual as png at a specified resolution
    Enter fig_id to specify what you would like your figure to be called.
    Other paremeters have default values and can be altered if needed'''
    path = os.path.join(IMAGES_PATH, fig_id + "." + fig_extension)
    print("Saving figure", fig_id)
    if tight_layout:
        plt.tight_layout()
    plt.savefig(path, format=fig_extension, dpi=resolution, transparent=transparent)

# general function for cleaning columns
def clean_cols(df):
    df.columns = [x.lower().replace(" ","_") for x in df.columns]
    return df

# histogram function
def hist_func(df, col, title, xlabel):
    """
    Provide df and column xlabel and title 
    to produce histogram
    """
    sns.histplot(df[col], binwidth=1)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.show()

# function for bar plot
def bar_horiz(df, colx, coly, xlabel, title, ylabel = "",
              figsize=(14,12), titlesize=20, palette = "Blues"):
    """
    Plots horizontal bar chart.
    Pass df, x, y, xlabel, title
    Defaults ylabel = "", figsize, titlesize and palette
    """
    sns.set_theme(context="notebook", 
                  style="whitegrid",
                 font_scale=1.5)
    palette = sns.color_palette(palette, n_colors=df[coly].count())
    palette.reverse()
    plt.figure(figsize=figsize)
    sns.barplot(data=df,
                x=df[colx],
                y=df[coly],
                orient="h",
               palette=palette)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title, fontsize=titlesize)
    save_fig(title.lower().replace(' ', '_'))
    plt.show()

    # function to create ratio columns
def ratio_func(df,col1_list,col2_list,new_col_list):
    """
    This function will create a new column that is a ratio of col1 / col2
    Pass list of cols to create multiple ratio cols simultaneously
    """
    for (col1, col2, new_col) in zip(col1_list, col2_list, new_col_list):
        df[new_col] = df[col1] / df[col2]

# function that can easily recreate map given parameters
def create_choropleth_map(df, col, color_map, title, vmax):
    '''
    Takes input of dataframe, column, cmap, title and vmax. 
    Creates choropleth map with colorbar.
    '''
    # get continental us shp for boundaries for map
    drop_continental = ["Alaska", "Hawaii"]
    gdf_cont = df[~df["state"].isin(drop_continental)]
    
    # set color min
    vmin = 0
    # create map figure and axes
    fig, ax = plt.subplots(figsize=(50,40))
    # call .plot() method on df
    ax = df.plot(column = col, 
                            cmap=color_map, 
                            ax=ax,
                            vmin=vmin,
                            vmax=vmax,
                            edgecolor='k',
                            legend=True,
                            legend_kwds={'shrink': 0.7},
                            missing_kwds={
                                "color": "lightgrey",
                            })
    # figure has two axes, cb is 2nd
    cb = fig.axes[1]
    # # set params for cb
    cb.tick_params(labelsize=60,
                      direction='out', 
                      length=6, 
                      width=2,
                      grid_alpha=1)
    # add annotation
    ax.annotate("•", xy=(0, .15), size=100, xycoords='figure fraction', color='lightgrey')
    ax.annotate("Missing Values", xy=(0.025, .155), size=70, xycoords='figure fraction')
    ax.annotate('Source: Gun Violence Archive - https://www.gunviolencearchive.org', 
            xy=(0, .125), xycoords='figure fraction', fontsize=50, color='#555555')
    # set map title
    ax.set_title(title, fontdict={'fontsize': 90}, loc='center')
    # set map extent
    xlim = ([gdf_cont.total_bounds[0],gdf_cont.total_bounds[2]])
    ylim = ([gdf_cont.total_bounds[1],gdf_cont.total_bounds[3]])
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    # remove axis surrounding map
    ax.set_axis_off()
    save_fig(title.lower().replace(' ', '_'))
    plt.show()

# function to create interactive folium map
def interactive_choro(gdf, shpfile,col_key_val_list, tooltip_col_list, tooltip_name_list,
                     popup_col_list, popup_name_list, fill_color="Blues", 
                      tiles="OpenStreetMap", legend_name = "Data Points"):
    """
    Function that takes in GeoDataframe, Column Key and Value,
    Tooltip/Popup list and name list (must be same length)
    Default values are: fill_color, tiles and legend_name
    """
    # basemap
    # f = folium.Figure(width=680, height=450)
    m = folium.Map([38, -99], 
                   maxZoom=10,
                   minZoom=3,
                   zoom_control=True,
                   zoom_start=4,
                   scrollWheelZoom=True,
    #                maxBounds=[[40, 68],[6, 97]],
                   tiles=tiles,
                   dragging=True)

    # popup
    popup = folium.features.GeoJsonPopup(
        fields=popup_col_list,
        aliases=popup_name_list, 
        localize=True,
        labels=True,
        style="background-color: grey;",
    )
    # tooltip
    tooltip = folium.features.GeoJsonTooltip(
        fields=tooltip_col_list,
        aliases=tooltip_name_list,
        localize=True,
        sticky=False,
        labels=True,
        style="""
            background-color: #F0EFEF;
            border: 1px solid black;
            border-radius: 3px;
            box-shadow: 3px;
        """,
        max_width=800,
    )
    
    # add choropleth layer
    g = folium.Choropleth(
        geo_data=shpfile,
        data=gdf,
        nan_fill_color="grey",
        nan_fill_opacity=0.5,
        columns=col_key_val_list,
        key_on='properties.state',
        fill_color=fill_color,
        fill_opacity=0.7,
        line_opacity=0.4,
        legend_name=legend_name,
        highlight=True,
    ).add_to(m)


    folium.GeoJson(
        gdf,
        style_function=lambda feature: {
    #         'fillColor': '#ffff00',
    #         'color': 'black',
            'weight': 0.2,
            'dashArray': '5, 5'
        },
        tooltip=tooltip,
        popup=popup).add_to(g)
    
    return m

# function to create day, month, year, weekday and day name from date column
def date_column(df, datecol):
    """
    Pass datetime column and crate new cols in df:
    - day, month, year, weekday, dayname
    """
    # define seasons
    Winter = ["Dec", "Jan","Feb"]
    Spring = ["Mar", "Apr","May"]
    Summer = ["Jun", "Jul", "Aug"]
    Autumn = ["Sep", "Oct","Nov"]
    
    # extract date info
    if pd.api.types.is_datetime64_dtype(df[datecol]):
        df["day"] = df[datecol].dt.day
        df["month"] = df[datecol].dt.month
        df["monthname"] = df["month"].apply(lambda x: calendar.month_abbr[x])
        df["monthtype"] = np.where(df["monthname"].isin(Winter),"Winter",
                                  np.where(df["monthname"].isin(Spring), "Spring",
                                          np.where(df["monthname"].isin(Summer),"Summer",
                                                  np.where(df["monthname"].isin(Autumn),"Autmn",'NA'))))
        df["year"] = df[datecol].dt.year
        df["dayofweek"] = df[datecol].dt.weekday
        df["dayname"] = df[datecol].dt.day_name()
        df["daytype"] = np.where(df["dayofweek"] >= 5,"Weekend","Weekday")
    else:
        print("Please pass datetime column")

if __name__ == '__main__':
    None
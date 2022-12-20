#!/usr/bin/env/ python
# import packages
import folium

# function to create interactive folium map
def interactive_choro(gdf, col_key_val_list, tooltip_col_list, tooltip_name_list,
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
        geo_data=gdf,
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
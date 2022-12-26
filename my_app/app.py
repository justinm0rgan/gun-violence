# import packages
import pandas as pd
import geopandas as gpd
from shiny import App, reactive, ui
from shinywidgets import output_widget, render_widget
import json
from branca.colormap import linear

# import functions
import shiny_functions as sf

# import data
df = pd.read_pickle('data//df_yr_mon_state')
us_shp = gpd.GeoDataFrame(pd.read_pickle('data/us_shp'))
df_gun_laws = pd.read_pickle('data/df_gun_laws')
df_census = pd.read_pickle('data/df_us_census')

# set variables
# start and end date
start_date = min(df["date"])
end_date = max(df["date"])
# legend color dict
legend_color_dict = {
    "count_per_1k":linear.Blues_07.colors,
    "injured_per_1k":linear.Greens_07.colors,
    "killed_per_1k":linear.Reds_07.colors}
# map color dict
map_color_dict = {
    "count_per_1k":linear.Blues_07,
    "injured_per_1k":linear.Greens_07,
    "killed_per_1k":linear.Reds_07}
# radio button dict
radio_button_dict={"count_per_1k":"Shooting per 1k", 
    "injured_per_1k":"Injured per 1k", "killed_per_1k":"Killed per 1k"}

app_ui = ui.page_fluid(
    ui.h1({"style": "text-align: center;"}, "Mass Shootings in the US"),
    output_widget("map"),
        ui.row(
            ui.h3("Methodology"),
            ui.p("All data on Mass Shootings is from the",\
                ui.a("Gun Violence Archive (GVA)", href="http://www.gunviolencearchive.org", target="_blank"),
                ui.tags.i("(Oct, 2019 - Dec, 2022)"),
                ", gun law data from ",ui.a("State Firearm Laws",href="https://www.statefirearmlaws.org/state-state-firearm-law-data", target="_blank"),
                ui.tags.i("(as of 2020)"),
                " and census data from: ",ui.a("Census.gov.", href="https://www.census.gov/en.html", target="_blank"),
                ui.tags.i("(American Community Survey 2016-2020 5yr estimate)"),
                ui.p("GVA uses a purely statistical threshold to define mass shooting based on the \
                    numeric value of",ui.tags.b("4 or more shot or killed, not including the shooter."),"They do not \
                    parse the definition to remove any subcategory of shooting. Therefore, they do not \
                    exclude, set apart, caveat, or differentiate victims based upon the circumstances \
                    in which they were shot. They believe equal importance is given to the counting \
                    of those injured as well as killed in a mass shooting incident.")
                    ),
        ui.row(
            ui.column(
                6,
                ui.h5("Directions:"),
                ui.p("Hover over states and/or click for more info. Select radio buttons to toggle between mass shooting incident count, injured and killed. \
                    Default map is complete range (10/2019-12/2022) of source data. \
                    If you would like to change timeframe, select date range drop down and press button."),
                ui.p("Please note, data will take a few seconds to recalculate"),
            ),
            ui.column(
                2,
                # radio button selection
                ui.input_radio_buttons("maptype","Select Metric",radio_button_dict),
            ),
            ui.column(1,
                ui.input_action_button("computedate","Change Date")
            ),
            ui.column(
                3,
                # date range input
                ui.input_date_range("daterange","Date range:",
                                    start=start_date,
                                    end=end_date,
                                    min=start_date,
                                    max=end_date, 
                                    format="yyyy-M-dd")
            ),
        ),
    ),
)

def server(input, output, session):
    @reactive.Calc
    def datechange():
        df_input=df[(df["date"] >= input.daterange()[0]) & (df["date"] < input.daterange()[1])]
        return df_input
    
    @output
    @render_widget
    def map():
        input.computedate()
        # add rgb to list
        map_color = input.maptype()
        rgb_list = sf.rgb_to_hex(legend_color_dict[map_color])

        # # filter df by user input
        # df_input=df[(df["date"] >= input.daterange()[0]) & (df["date"] < input.daterange()[1])]

        # sum up variables for plot
        # group subset by state
        # create variables for function
        with reactive.isolate():
            groupby_list = ["state"]
            agg_dict = {"count":"sum","#_injured":"sum","#_killed":"sum","total_injured_killed":"sum"}
            sort_list = ["count","#_injured","#_killed"]
            # apply function
            df_input = sf.groupby_mult(datechange(), groupby_list, agg_dict, sort_list)

            # join census data
            df_input = df_input.merge(df_census, how="outer")

            # get ratio per state
            # create lists for function
            col_list = ["count","#_injured", "#_killed", "total_injured_killed"]
            new_col_list = ["count_per_1k", "injured_per_1k","killed_per_1k","total_per_1k"]
            # apply function
            sf.rate_per_1k(df_input, col_list, new_col_list)

            # create divide metric
            metric=sf.divide_metric(df_input,input.maptype())

            # join with gun laws
            df_input = df_input.merge(df_gun_laws, how="outer")
            gdf = gpd.GeoDataFrame(df_input.merge(us_shp, left_on="state", right_on="name"))
            # reset index
            gdf.set_index("state_fips", inplace=True)

            # format pop cols
            gdf["population"]=gdf["population"].map('{:,.0f}'.format)
            gdf["pop_per_1k"]=gdf["pop_per_1k"].map('{:,.0f}'.format)

            # create GeoJSON from gdf
            geojson_gdf=gdf.to_json()
            geojson_gdf=json.loads(geojson_gdf)

            # select name for plot
            title = input.maptype()
            title = radio_button_dict[title]

            # use function to plot
            return sf.int_choro_ipyleaflet(geojson_gdf, gdf=gdf, 
            value=input.maptype(),title=title,metric=metric, rgb_list=rgb_list, colormap=map_color_dict[map_color])
    
app = App(app_ui, server)

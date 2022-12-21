# pip libraires
import numpy as np
import json
import pandas as pd
import csv

# visualization librairies
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from ast import literal_eval

# Plotly
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from jupyter_dash import JupyterDash
from dash import Dash, dcc, html, Input, Output, State
import dash_leaflet as dl
import dash_leaflet.express as dlx
import dash
from dash_extensions.javascript import assign
from dash.exceptions import PreventUpdate

# Load the dataframes
df_summaries_region = pd.read_csv('df_summaries_region.csv', index_col=0)
df_summaries_coordinates = pd.read_csv('df_summaries_coordinates.csv', index_col=0)

# Create a new column for positive and negative sentiment of regions, and normalize the sentiment score by country production
df_region_grouped = df_summaries_region.groupby(['Movie_release', 'region']).sum().reset_index()
df_region_grouped[['general_sentiment', 'pos', 'neg', 'positive_sentiment', 'negative_sentiment']] = \
    df_region_grouped[['general_sentiment', 'pos', 'neg', 'positive_sentiment', 'negative_sentiment']].div(df_region_grouped['production'], axis=0)

# Normalise the production by year to get the percentage of production compared to the total world production
prod_by_year = df_region_grouped.groupby(['Movie_release']).sum().reset_index()
df_region_grouped['production'] /= df_region_grouped['Movie_release'].map(prod_by_year.set_index('Movie_release')['production'])

# Create a new column for positive and negative sentiment of countries, and normalize the sentiment score by country production
df_country_grouped = df_summaries_region.groupby(['Movie_release', 'countries']).sum().reset_index()
df_country_grouped[['general_sentiment', 'pos', 'neg', 'positive_sentiment', 'negative_sentiment']] = \
    df_country_grouped[['general_sentiment', 'pos', 'neg', 'positive_sentiment', 'negative_sentiment']].div(df_country_grouped['production'], axis=0)

# Normalise the production by year to get the percentage of production compared to the total world production
df_country_grouped['production'] /= df_country_grouped['Movie_release'].map(prod_by_year.set_index('Movie_release')['production'])

# Create a JSON string in the geojson format for the map   
feature_collection = {
    'type': 'FeatureCollection',
    'features': []
}

# Loop through the rows of the DataFrame
for _, row in df_summaries_coordinates.iterrows():
    # Create a feature for each country and year
    feature = {
        'type': 'Feature',
        'properties': {
            'time': row['Movie_release'],
            'descript_prodion': row['countries'],
            'sentiment':row['general_sentiment'],
            'name': row['Movie_name_y'],
        },
        'geometry': {
            'type': 'Point',
            'coordinates': [row['longitude'], row['latitude']]
        }
    }

    # Add the feature to the feature collection
    feature_collection['features'].append(feature)
    
# Define the year and the range displayed on the sliders
slider_year = 2000
range_year = 1995

# Define the map type
card_type = dl.TileLayer(
                            url='https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png',
                            attribution='&copy; <a href="https://stadiamaps.com/">Stadia Maps</a>, &copy; <a href="https://openmapt_prodiles.org/">OpenMapt_prodiles</a> &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors',
                        )

# Format the dataset to be used in the map
df_summaries_coordinates = df_summaries_coordinates[df_summaries_coordinates['Movie_release'] >= 1900]
df_summaries_coordinates=df_summaries_coordinates.dropna(subset=['countries','latitude'])

# Define color scale gradient
colorscale = ['red', 'yellow', 'green']

# Define the color scale
chroma = "https://cdnjs.cloudflare.com/ajax/libs/chroma-js/2.1.0/chroma.min.js"  # js lib used for colors
color_prop = 'general_sentiment' # property to color by

# Create a colorbar for the sentiment score
vmax = 1
vmin = -1
colorbar = dl.Colorbar(colorscale=colorscale, width=20, height=150, min=-1, max=1, unit=' sentiment score', style= {'color': 'white'})


# Javascript code for Geojson rendering logic

point_to_layer = assign("""
function(feature, latlng, context){
    const {min, max, colorscale, circleOptions, colorProp} = context.props.hideout;
    const csc = chroma.scale(colorscale).domain([min, max]);  // chroma lib to construct colorscale
    circleOptions.fillColor = csc(feature.properties[colorProp]);  // set color based on color prop.
    return L.circleMarker(latlng, circleOptions);  // sender a simple circle marker.
}""")

cluster_to_layer = assign("""function(feature, latlng, index, context){
    const {min, max, colorscale, circleOptions, colorProp} = context.props.hideout;
    const csc = chroma.scale(colorscale).domain([min, max]);

    // Set color based on mean value of leaves.
    const leaves = index.getLeaves(feature.properties.cluster_id);
    let valueSum = 0;
    for (let i = 0; i < leaves.length; ++i) {
        valueSum += leaves[i].properties[colorProp]
    }
    const valueMean = valueSum / leaves.length;
    
    // Render a circle with the number of leaves written in the center.
    const icon = L.divIcon.scatter({
        html: '<div style="background-color:white;"><span>' + feature.properties.point_count_abbreviated + '</span></div>',
        className: "marker-cluster",
        iconSize: L.point(40, 40),
        color: csc(valueMean)
    });
    return L.marker(latlng, {icon : icon})
}""")

def get_data(subset:object)->list:
    """ Returns the map layout and the data to be displayed on the map from the input subset.
    Args:
        x (object): dataframe subset to be displayed on the map

    Returns:
        card_type: The background map type
        geojson: The data to be displayed on the map
        colorbar: The colorbar to be displayed on the map
    """

    # Pre process the data into geobuf.
    dicts = subset.to_dict('rows')

    # Add tooltip to each point. The tooltip is the name of the country, the sentiment and the year.
    for row in dicts:
        row["tooltip"] = "{} ({:.1f})".format(str(int(row['Movie_release'])) + ',  ' + row['Movie_name_y'] + ' ', row[color_prop])  # bind tooltip

    geojson = dlx.dicts_to_geojson(dicts, lon="longitude", lat = "latitude")  # convert to geojson
    geobuf = dlx.geojson_to_geobuf(geojson)  # convert to geobuf

    # Create geojson.
    geojson = dl.GeoJSON(data=geobuf, id="geojson", format="geobuf",
                        zoomToBounds=False,  # when true, zooms to bounds when data changes
                        cluster=True,  # when true, data are clustered
                        clusterToLayer=cluster_to_layer,  # how to draw clusters
                        zoomToBoundsOnClick=True,  # when true, zooms to bounds of feature (cluster, marker, etc.) on click
                        options=dict(pointToLayer=point_to_layer),  # how to draw points
                        superClusterOptions=dict(radius=120),   # adjust cluster size
                        hideout=dict(colorProp=color_prop, circleOptions=dict(fillOpacity=1, stroke=False, radius=5),
                                    min=vmin, max=vmax, colorscale=colorscale)) # hideout is used in the point_to_layer function

    return [card_type, geojson, colorbar]

# initialise color chart to use for the plots
color_chart = px.colors.qualitative.Plotly

# Define the list of countries that will be in the checklist, and the ones that start checked
country_checklist = [['United States', 'United Kingdom', 'France', 'India', 'Germany', 'Australia', 'Italy', 'China', 'Japan', 'Canada', 'Mexico', 'Spain', 'Russia', 'Iraq', 'Vietnam', 'Netherlands', 'Austria', 'Luzon', 'Turkey', 'Switzerland', 'South Korea', 'Brazil', 'Poland', 'Sweden', 'Egypt_prod', 'Israel', 'Argentina', 'Afghanistan', 'New Zealand'],
 ['Vietnam', 'Afghanistan', 'Iraq']]

# Define the list of regions that will be in the checklist, and the ones that start checked
region_checklist = [[
'Middle East',
'Soviet union',
'Africa',
'Oceania',
'PIGS',
'North America',
'Latin America',
'Continental Europe',
'South Asia',
'South East Asia',
'East Asia',
'North Asia',
'Scandinavia',], ['South Asia', 'Middle East', 'Continental Europe']]

# Create the map htmp layer with initial values
map_layer = html.Div([

    dl.Map(get_data(df_summaries_coordinates[df_summaries_coordinates['Movie_release'].between(range_year, slider_year)]),

     id='world_map', zoom = 4, center=(40.0884, -3.68042)),

], style={'width': '100%', 'height': '80vh', 'margin': "auto", "display": "block", "position": "relative"})

# Create the app
app = Dash(__name__)

# Define the layout of the app in html
app.layout = html.Div([
    ################ Graph ##################
    html.H4("Country production and sentiment analysis graphs"),
    html.P("Select country or region mode."),
    dcc.Dropdown(
        id='country_continent',
        options=['Country', 'Regions'],
        value='Country'
    ),
    html.P("Select desired countries.", id = "country_continent_text"),
    dcc.Checklist([],[],
      id='checklist',
      labelStyle={'display': 'block'},
      style={'columnCount': 7}
      ),
    html.P("Select sentiment or movie production analysis."),
    dcc.Dropdown(
        id='sentiment_prod',
        options=['Sentiment', 'Production'],
        value='Sentiment'
    ),
    dcc.Graph(id="graph"),
    ################ MAP ##################
    html.H4("Country production and sentiment map"),
    html.P("Select Year Range to analyze the sentiment and filming location of the movies in those years."),

    dcc.Checklist(
    ['Fixed Range'],
    [],
    id='fixed_range',
    ),

    dcc.RangeSlider(min=1900, max=2015,
      step=1, value=[range_year, slider_year],
      marks={i: '{}'.format(i) for i in range(1900, 2015, 5)},
      tooltip={"placement": "bottom", "always_visible": True},
      id='range_slider',
    ),
      
    map_layer
])

# Define the callback to change the checklist depending on the mode selected
@app.callback(
    [Output("checklist", 'options'),
    Output("checklist", 'value'),
    Output("country_continent_text", "children"), ],
    Input("country_continent", "value"))
def change_mode(contry_continent):
    if contry_continent == "Country":
        
        text = "Select desired countries."
        return country_checklist[0], country_checklist[1], text
    else :
        
        text = "Select desired regions."
        return region_checklist[0], region_checklist[1], text

# Define the callback to change the graph depending on the mode selected
@app.callback(
    Output("graph", "figure"),  
    [Input("country_continent", "value"),
    Input("checklist", "value"),
    Input("sentiment_prod", "value")])
def display_area(contry_continent, checks, sentiment_prod):
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    df = pd.DataFrame()
    
    # define the dataframe to use depending on the mode selected
    if contry_continent == "Country":
        mode = "countries"
        df = df_country_grouped[df_country_grouped[mode].isin(checks)].fillna(0)
    else :
        mode = "region"
        df = df_region_grouped[df_region_grouped[mode].isin(checks)].fillna(0)

    # If the sentiment analysis is selected, plot the sentiment score in symmetric stacked area plots
    if sentiment_prod == "Sentiment":
        axis_label = "Average positive(y>0) and negative(y<0) <br> sentiment score."
        # Iterate through selected countries or regions
        for i, c in enumerate(checks):
            
            # Plot the positive sentiment score
            fig.add_trace(go.Scatter(
                name = c,
                x = df[df[mode] == c]["Movie_release"],
                y = df[df[mode] == c]["pos"],
                line_color= color_chart[i],
                fillcolor= color_chart[i],
                legendgroup= i,
                stackgroup='one',
            ))
            # Plot the negative sentiment score
            fig.add_trace(go.Scatter(
                name = c,
                x = df[df[mode] == c]["Movie_release"],
                y = df[df[mode] == c]["neg"],
                line_color= color_chart[i],
                fillcolor= color_chart[i],
                legendgroup= i,
                showlegend=False,
                stackgroup='two'
            ))
    # If the production analysis is selected, plot the production in stacked area plots
    else :
        axis_label = "Ratio of movies produced in a country <br> by total productions."

        # Iterate through selected countries or regions
        for c in checks:
            # Plot the production per year
            fig.add_trace(go.Scatter(
                name = c,
                x = df[df[mode] == c]["Movie_release"],
                y = df[df[mode] == c]["production"],
                showlegend=True,
                legendgroup= 0,
                stackgroup='three'
            ))
    # Define the layout of the graph and the tiles
    fig.update_layout(
    title="Evolution of movie " + str(sentiment_prod) + " by " + str(contry_continent),
    xaxis_title="Year",
    yaxis_title= axis_label,
    legend_title=str(contry_continent),
    )

    # Add a horizontal line at y=0
    fig.add_hline(y=0, line_width=1, line_color="black")
    
    return fig

# Create global variables to store the range difference, used when the fixed range is selected.
range_difference = 5

# app callback to update the map when the slider is moved.
@app.callback(
    [Output("world_map", "children"),
    Output("range_slider", "value")],

    [Input("range_slider", "value"),
    Input("fixed_range", "value")],)
def display_area(year_range, fixed_value):

    global slider_year
    global range_difference
    new_range = []

    # If the fixed range is not selected, return the data subset for the selected range.
    if len(fixed_value) == 0 :
        range_difference = year_range[1] - year_range[0]
        return get_data(df_summaries_coordinates[df_summaries_coordinates['Movie_release'].between(year_range[0], year_range[1])]), [year_range[0], year_range[1]]

    # If the fixed range is selected, move the sliders accordingly and return the data subset for the new range.
    else:
        # If the slider is moved to the right, move the range to the right.
        if slider_year != year_range[0] :
            new_range = [year_range[0], year_range[0] + range_difference]
            slider_year = new_range[0]

        # If the slider is moved to the left, move the range to the left.
        elif slider_year + range_difference != year_range[1] :
            new_range = [year_range[1] - range_difference, year_range[1]]
            slider_year = new_range[0]
        # Return the data subset for the new range.
        return get_data(df_summaries_coordinates[df_summaries_coordinates['Movie_release'].between(new_range[0], new_range[1])]), [new_range[0], new_range[1]]

# Run the app.
app.run_server(mode='inline', port=8050)
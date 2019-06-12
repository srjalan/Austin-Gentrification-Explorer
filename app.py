# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 10:36:48 2019

@author: rsong
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
import json
import copy

# Read in data

df_geo_data = pd.read_csv('data/austin_lon_lat_data.csv')
df_stats_data  = pd.read_csv('data/austin_stats_data.csv')

# Define constants

YEARS = [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]
LAT = 30.3
LON = -97.7431
ZOOM = 10.25
METRICS = ['Predicted Score', 'Vulnerability Score']
TRACT_STATS = ['Ethnicity Composition', 'Education Achievement','Median Income','Renter Percentage', 'ALN - Number of Rental Units', 'ALN - Rent Per Unit', 'ALN - Rent Per Sq Ft', 'ALN - Median Occupancy','Vulnerability Score','Predicted Score']
TRACT_STATS_LABELS = ['Percentage of Non-white Residents', 'Percentage of Post-secondary Education','Median Income','Percentage of Renters','ALN - Number of Rental Units', 'ALN - Rent Per Unit', 'ALN - Rent Per Sq Ft', 'ALN - Median Occupancy','Vulnerability Score','Predicted Score']

external_stylesheets = ["https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css"]

# Dash app

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Austin Gentrification Explorer"
server = app.server 

app.config.supress_callback_exceptions = True

colorscale = ['#969696', '#f7fcfd','#e5f5f9','#ccece6','#99d8c9','#66c2a4','#41ae76','#238b45','#005824']

mapbox_access_token = "pk.eyJ1IjoiamFja3AiLCJhIjoidGpzN0lXVSJ9.7YK6eRwUNFwd3ODZff6JvA"

'''
~~~~~~~~~~~~~~~~~~~~~~
~~ Initial Map Data ~~
~~~~~~~~~~~~~~~~~~~~~~
'''

map_data = [dict(
        lat=df_geo_data['rep_point_lat'],
        lon=df_geo_data['rep_point_lon'],
        mode='markers',
        type = 'scattermapbox',
        text = df_geo_data['FIPS'].astype(str),
        hoverinfo = 'text',
        marker = dict(size=5, color='white', opacity=0)
)]
map_layout = dict(
    #clickmode = 'event+select',
    margin=dict(
        l=0,
        r=35,
        b=30
    ),
    height=600,
    #width = 1200,
    title='<b>'+METRICS[0]+' Heatmap'+'</b><br>(Click map to see tract-level statistics)',
    titlefont=dict(family='Helvetica'),
    mapbox=dict(
        layers=[],
        accesstoken=mapbox_access_token,
        center=dict(
            lat=LAT,
            lon=LON
        ),       
        pitch=0,
        zoom=ZOOM,
        style='streets'
    ),
    uirevision='same'
)

map_fig = dict(data=map_data, layout=copy.deepcopy(map_layout)) 

'''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~ Initial Histogram Data ~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''
df_temp=df_stats_data[df_stats_data['FIPS']==np.int('48453001100')]
df_temp=df_temp[df_temp['year']<2018]
df_temp=df_temp[df_temp['year']>2012]
histogram_data = [dict(
            x=df_temp['year'],
            y=df_temp[TRACT_STATS_LABELS[0]],
            type = 'bar',
            marker=dict(color='#005824', opacity=0.75)
    )]

histogram_layout = dict(
    margin=dict(
        l=35,
        r=0,
        b=35
    ),
    height=600,
    title='<b>'+'Tract 48453001100: ' + TRACT_STATS_LABELS[0]+'</b>',
    titlefont=dict(family='Helvetica')
)

histogram_fig = dict(data=histogram_data, layout=copy.deepcopy(histogram_layout))

'''
~~~~~~~~~~~~~~~~
~~ APP LAYOUT ~~
~~~~~~~~~~~~~~~~
'''

app.layout = html.Div([
    # Title - Row
    html.Div(
        [
            html.H1(
                'Austin Gentrification Explorer',
                style={'font-family': 'Helvetica',
                       "margin-top": "25",
                       'padding-top': 10,
                       "margin-bottom": "0"},
                className='eight columns',
            ),
            html.Img(
                #src="https://i.ibb.co/v14GbJ4/gatech-logo.png",
                src = "https://i.ibb.co/zHR1gPp/gatech-logo2.png",
                className='two columns',
                style={
                    'height': '15%',
                    'width': '15%',
                    'float': 'right',
                    'position': 'relative',
                    'padding-top': 10,
                    'padding-right': 0
                },
            ),
            html.P(
                'A Visualization of Austin Gentrification Study',
                style={'font-family': 'Helvetica',
                       "font-size": "120%",
                       "width": "80%"},
                className='eight columns',
            ),
        ],
        className='row'
    ),

    # Selectors
    html.Div(
        [
            html.Div(
                [
                    html.P('Drag the slider to change the year:'),
                    dcc.Slider(
                        id='years-slider',
                        min=min(YEARS),
                        max=max(YEARS),
                        value=min(YEARS),
                        marks={str(year): str(year) for year in YEARS},
                    ),
                ],
                className='three columns',
                style={'margin-top': 10,
                       'margin-left': 5,
                        }
            ),               
            html.Div(
                [
                    html.P('Study Metrics:'),
                    dcc.Dropdown(
                        id='map_update',
                        options=[{'label': metric, 'value': i} for i,metric in enumerate(METRICS)],
                        value=0
                    )
                ],
                className='two columns',
                style={'margin-top': 10,
                       'margin-left': 100}
            ),
            html.Div([],
                className='one column',
                style={'margin-top': 10}
            ),
            html.Div(
                [
                    html.P('Tract-level Statistics:'),
                    dcc.Dropdown(
                        id='histogram_update',
                        options=[{'label': tract_stats, 'value': i} for i,tract_stats in enumerate(TRACT_STATS)],
                        value=0
                    )
                ],
                className='three columns',
                style={'margin-top': 10,
                       'margin-left': 5}
            ),         
        ],
        className='row',
        style={'padding-top': 20},
    ),

    # Map + Histogram
    html.Div(
        [
            html.Div(
                [
                    dcc.Graph(id='dynamic_choropleth_map',
                        clickData={'points': [{'customdata': 48453001100}]},
                        figure = map_fig,
                        config={'scrollZoom': True})
                ], className = "six columns"
            ),
            html.Div(
                [
                    dcc.Graph(
                        id='dynamic_histogram',
                        figure=histogram_fig
                    )
                ],className="six columns"),
            html.Div([
                html.P('† Vulnerability scores are computed based on UT Austin 2018 Gentrification Study for comparison purposes.'),
            ],className="six columns"),
            html.Div([
                html.P('† Proprietary rental data are provided by ALN Apartment Data.'
                )
            ],className="five columns")
        ], className="row",
           style={'padding-top': 20},)
], className='ten columns offset-by-one')

'''
~~~~~~~~~~~~~~~
~~ CALLBACKS ~~
~~~~~~~~~~~~~~~
'''
# Slider bar callback

@app.callback(
    [Output('years-slider', 'min'),
     Output('years-slider', 'max'),
     Output('years-slider', 'value'),
     Output('years-slider', 'marks')],
    [Input('map_update', 'value')],
    [State('years-slider', 'value')])
def update_slider(metric, slider_value):
    if metric == 0:
        min_year=min(YEARS)
        max_year=max(YEARS)
        value=slider_value
        marks={str(year): str(year) for year in YEARS}
    else:
        min_year=min(YEARS[:5])
        max_year=max(YEARS[:5])
        if slider_value in YEARS[:5]:
            value=slider_value
        else:
            value=max(YEARS[:5])
        marks={str(year): str(year) for year in YEARS[:5]}        
    return min_year, max_year, value, marks

# Map callback

@app.callback(
        Output('dynamic_choropleth_map', 'figure'),
        [Input('years-slider', 'value'),
         Input('map_update', 'value')],
        [State('dynamic_choropleth_map', 'figure')])
def display_map(year, metric, figure):

    df_temp1=df_stats_data[df_stats_data['year']==year][['FIPS',METRICS[metric]]]
    df_temp1 = pd.merge(df_geo_data, df_temp1, on='FIPS', how='left')

    data = [dict(
            lat=df_temp1['rep_point_lat'],
            lon=df_temp1['rep_point_lon'],
            mode='markers',
            type = 'scattermapbox',
            customdata = df_temp1['FIPS'].astype(str),
            text = 'Tract ID: '+df_temp1['FIPS'].astype(str) +'<br>'+METRICS[metric]+': '+np.round(df_temp1[METRICS[metric]],2).astype(str),
            hoverinfo = 'text',
            marker = dict(size=5, color='white', opacity=0.0)
    )]

    layout = copy.deepcopy(map_layout)
    layout['title'] = '<b>'+METRICS[metric]+' Heatmap'+'</b><br>(Click map to see tract-level statistics)'
    
    # load geojson for each census tract
    for i in range(len(colorscale)):
        try:
            with open('data/'+METRICS[metric]+'/'+str(year)+'/austin'+str(i)+'.geojson') as f:
                geo_data = json.load(f)
            geo_layer = dict(
                sourcetype = 'geojson',
                source = geo_data,
                type = 'fill',
                color = colorscale[i],
                opacity = 0.6
            )
            layout['mapbox']['layers'].append(geo_layer)
        except:
            pass
    
    fig = dict(data=data, layout=layout)

    return fig

# Histogram callback

@app.callback(
    Output('dynamic_histogram', 'figure'),
    [Input('dynamic_choropleth_map', 'clickData'),
     Input('histogram_update', 'value')],
    [State('dynamic_histogram', 'figure')])
def display_histogram(clickData, stats, figure):

    FIPS = str(clickData['points'][0]['customdata'])

    df_temp1=df_stats_data[df_stats_data['FIPS']==np.int(FIPS)]
    if stats<4 or stats ==8:
        df_temp1=df_temp1[df_temp1['year']<2018]
    if stats>3 and stats <8:
        df_temp1=df_temp1[df_temp1['year']<2020]

    data = [dict(
                x=df_temp1['year'],
                y=df_temp1[TRACT_STATS_LABELS[stats]],
                type = 'bar',
                marker=dict(color='#005824', opacity=0.75)
        )]

    layout = copy.deepcopy(histogram_layout)
    layout['title'] = '<b>'+'Tract '+FIPS+': ' + TRACT_STATS_LABELS[stats]+'</b>'

    fig = dict(data=data, layout=layout)    

    return fig
    
# Dash app launcher
if __name__ == '__main__':
    app.run_server(debug=True,port=8020)
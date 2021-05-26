import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_table
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
import sys
import os
import pandas as pd
import numpy as np
import json
from datetime import datetime as dt
from glob import glob

from app import app

# def read_data(data_dir):
#     all_submissions = glob(data_dir)
#     # for ef in 

#     return(all_submissions)

# layout = html.P("This is the content of the home page!")

df = pd.DataFrame({
    'a': [1, 2, 3],
    'b': [4, 1, 4],
    'c': ['x', 'y', 'z'],
})

layout = html.Div([
    dcc.Dropdown(
        id='sim-dropdown',
        options=[{'label': i, 'value': i} for i in df['c'].unique()],
        value='a'
    ),
    html.Hr(),
    html.Div(id='sim-output'),
])

@app.callback(Output('sim-output', 'children'),
              [Input('sim-dropdown', 'value')])
def update_output_1(value):
    # Safely reassign the filter to a new variable
    filtered_df = df[df['c'] == str(value)]
    return len(filtered_df)
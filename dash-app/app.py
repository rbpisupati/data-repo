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
from plotly.subplots import make_subplots
import json
from datetime import datetime as dt
import dash_uploader as du


app = dash.Dash(external_stylesheets=[dbc.themes.LITERA], suppress_callback_exceptions=True)


SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
PROJECT_DIR = os.path.join( SCRIPT_DIR, '..' )
DATA_DIR = os.path.join( PROJECT_DIR, 'data/sample_sheets/' )
# sys.path.append(os.path.normpath(os.path.join(PROJECT_DIR, "app/scripts")))
# import data_submission as dbsub
# import data_viewer as dbview
from modules import data_submission as dbsub
from modules import data_viewer as dbview

du.configure_upload(app, DATA_DIR)

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Lab NGS Data Repository", className="display-4"),
        html.Hr(),
        html.P(
            "You could do look-up for samples which were sequenced already or make a new submission", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Look Up", href="/", active="exact"),
                dbc.NavLink("Submission", href="/submission", active="exact")
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return 
    elif pathname == "/submission":
        return dbsub.layout
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


if __name__ == '__main__':
    app.run_server(debug=True)

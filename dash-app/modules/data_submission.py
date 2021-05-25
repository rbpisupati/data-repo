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
import io
import flask
import dash_uploader as du
import uuid


from app import app

def upload_files(t_uuid):
    return(
        du.Upload(
            id='dash-uploader',
            text="Submit a CSV (comma separated file) file // maximum file size 8Mb",
            text_completed='Uploaded: ',
            upload_id=t_uuid,
            cancel_button=True,
            pause_button=False,
            filetypes=None,
            max_file_size=8,
            default_style=None,
            max_files=1,
        )
    )

t_uuid = uuid.uuid4()

layout = html.Div([
    # dbc.InputGroup(
    #         [
    #             dbc.InputGroupAddon("@", addon_type="prepend"),
    #             dbc.Input(id = "sub_submitter", placeholder="Username"),
    #         ],
    #         className="mb-3",
    #     ),
    dbc.InputGroup(
        [
            dbc.Input(id = "sub_submitter", placeholder="Submitter's username"),
            dbc.InputGroupAddon("@gmi.oeaw.ac.at", addon_type="append"),
        ],
        className="mb-3",
    ),
    dbc.InputGroup(
        [
            dbc.InputGroupAddon("Description", addon_type="prepend"),
            dbc.Input(id="sub_description", placeholder="text"),
        ],
        className="mb-3",
    ),
    dbc.InputGroup(
        [
            dbc.InputGroupAddon("Description", addon_type="prepend"),
            dbc.Input(id="sub_description", placeholder="text"),
        ],
        className="mb-3",
    ),
    # dbc.InputGroup(
    #     [
    #         dbc.InputGroupAddon("$", addon_type="prepend"),
    #         dbc.Input(placeholder="Amount", type="number"),
    #         dbc.InputGroupAddon(".00", addon_type="append"),
    #     ],
    #     className="mb-3",
    # ),
    # dbc.InputGroup(
    #     [
    #         dbc.InputGroupAddon("Master list", addon_type="prepend"),
            
    #     ],
    #     className="mb-3",
    # ),
    upload_files( t_uuid ),
])
# Description	User
	# samples	Coverage/Reads	Read mode	Library type	Date initial	Status	Date to NGS	NGS sample ID	NGS request #	Sent to	Date ready	Flowcell	Raw data location	Notes	iSeq Flowcell	iSeq Location


@app.callback(Output("sub_submitter_value", "children"), [Input("sub_submitter", "value")])
def output_text(value):
    return value
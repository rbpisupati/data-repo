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
    return( html.Div (
        [
            html.Div(
                [
                    du.Upload(
                        id='dash-uploader',
                        text="requires a comma separated file // maximum file size 8Mb",
                        text_completed='Uploaded: ',
                        upload_id=t_uuid,
                        cancel_button=True,
                        pause_button=False,
                        filetypes=None,
                        max_file_size=8,
                        default_style=None,
                        max_files=1,
                    ),
                    html.Div(id='callback-output'),
                ],
                style={  # wrapper div style
                    'textAlign': 'center',
                    # 'width': '600px',
                    'padding': '20px',
                    'display': 'inline-block'
                }),
        ],
        style={
            'textAlign': 'center',
        },
    ))

t_uuid = uuid.uuid4()
def_metadata = {
"sub_submitter": None,
"sub_description": None,
"sub_library": None,
"sub_readmode": None,
"sub_flowcellid": None,
"sub_ngssampleid": None,
"sub_requestid": None,
"sub_rawdatapath": None,
"sub_notes": None,
"sub_reset": None
}

layout = html.Div([
    html.H1( "Input Metadata" ),
    dbc.InputGroup(
        [
            dbc.Input(id = "sub_submitter", debounce=True, placeholder="Submitter's username"),
            dbc.InputGroupAddon("@gmi.oeaw.ac.at", addon_type="append"),
        ],
        className="mb-3",
    ),
    dbc.InputGroup(
        [
            dbc.InputGroupAddon("Description", addon_type="prepend"),
            dbc.Textarea(id="sub_description", debounce=True),
            # dbc.Input(, placeholder="text"),
        ],
        className="mb-3",
    ),
    dbc.InputGroup(
        [
            dbc.InputGroupAddon("Library type", addon_type="prepend"),
            dbc.Select(
                id="sub_library",
                options=[
                    {"label": "None", "value": "none"},
                    {"label": "Bisulfite", "value": "bsseq"},
                    {"label": "DNA-seq", "value": "dnaseq"},
                    {"label": "PacBio", "value": "pacbio"},
                    {"label": "RNA-seq", "value": "rnaseq"},
                    {"label": "ChiP-seq", "value": "chipseq"},
                    {"label": "TAG-seq", "value": "tagseq"},
                ],
            )
        ],
        className="mb-3",
    ),
    dbc.InputGroup(
        [
            dbc.InputGroupAddon("Read mode", addon_type="prepend"),
            dbc.Select(
                id="sub_readmode",
                options=[
                    {"label": "None", "value": "None"},
                    {"label": "PE50", "value": "PE50"},
                    {"label": "PE75", "value": "PE75"},
                    {"label": "PE100", "value": "PE100"},
                    {"label": "PE125", "value": "PE125"},
                    {"label": "PE150", "value": "PE150"},
                    {"label": "PE200", "value": "PE200"},
                    {"label": "PE300", "value": "PE300"},
                    {"label": "SE50", "value": "SE50"},
                    {"label": "SE75", "value": "SE75"},
                    {"label": "SE100", "value": "SE100"},
                    {"label": "SE150", "value": "SE150"},
                ],
            )
        ],
        className="mb-3",
    ),
    dbc.InputGroup(
        [
            dbc.InputGroupAddon("NGS Flowcell ID", addon_type="prepend"),
            dbc.Input(id="sub_flowcellid",debounce=True, placeholder="text"),
        ],
        className="mb-3",
    ),
    # dbc.InputGroup(
    #     [
    #         dbc.InputGroupAddon("NGS sample ID", addon_type="prepend"),
    #         dbc.Input(id="sub_ngssampleid", placeholder="text"),
    #     ],
    #     className="mb-3",
    # ),
    dbc.InputGroup(
        [
            dbc.InputGroupAddon("NGS request ID", addon_type="prepend"),
            dbc.Input(id="sub_requestid", debounce = True, type = "number", placeholder="numeric"),
        ],
        className="mb-3",
    ),
    dbc.InputGroup(
        [
            dbc.Input(id="sub_rawdatapath", debounce = True, placeholder="folder path to raw.data"),
            dbc.InputGroupAddon("Raw data location", addon_type="append"),
        ],
        className="mb-3",
    ),
    dbc.InputGroup(
        [
            dbc.InputGroupAddon("Short note on experimental design", addon_type="prepend"),
            dbc.Textarea(id="sub_notes", debounce=True),
            # dbc.Input(, placeholder="text"),
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
    # 
    dbc.InputGroup(
        [
            dbc.InputGroupAddon("Master list for multiplexed samples", addon_type="prepend"),
            upload_files( t_uuid ),
        ],
        className="mb-3",
    ),
    html.Hr(  ),
    html.Div([
        dbc.Button("Submit", outline=True, color="primary", className="mr-1"),
        dbc.Button("Reset",  outline=True, id = "sub_reset", color="danger", className="mr-2"),
    ]),
    # dcc.Store inside the app that stores the intermediate value
    dcc.Store(id='sub_submitter_final'),
    dcc.Store(id='sub_description_final'),
    dcc.Store(id='sub_library_final'),
    dcc.Store(id='sub_readmode_final'),
    dcc.Store(id='sub_flowcellid_final'),
    dcc.Store(id='sub_ngssampleid_final'),
    dcc.Store(id='sub_requestid_final'),
    dcc.Store(id='sub_rawdatapath_final'),
    dcc.Store(id='sub_notes_final'),
    dcc.Store(id='sub_reset_final'),

])


@app.callback(Output('sub_submitter_final', 'data'), [Input('sub_submitter', 'value'), Input("sub_reset", "n_clicks")])
def return_submitter_value(value, reset_click):
    if reset_click is None:
        return value
    else:
        return def_metadata['sub_submitter']

@app.callback(Output('sub_description_final', 'data'), [Input('sub_description', 'value'), Input("sub_reset", "n_clicks")])
def return_description_value(value, reset_click):
    if reset_click is None:
        return value
    else:
        return def_metadata['sub_description']

@app.callback(Output('sub_library_final', 'data'), [Input('sub_library', 'value'), Input("sub_reset", "n_clicks")])
def return_library_value(value, reset_click):
    if reset_click is None:
        return value
    else:
        return def_metadata['sub_library']

@app.callback(Output('sub_readmode_final', 'data'), [Input('sub_readmode', 'value'), Input("sub_reset", "n_clicks")])
def return_readmode_value(value, reset_click):
    if reset_click is None:
        return value
    else:
        return def_metadata['sub_readmode']

@app.callback(Output('sub_flowcellid_final', 'data'), [Input('sub_flowcellid', 'value'), Input("sub_reset", "n_clicks")])
def return_flowcellid_value(value, reset_click):
    if reset_click is None:
        return value
    else:
        return def_metadata['sub_flowcellid']

@app.callback(Output('sub_ngssampleid_final', 'data'), [Input('sub_ngssampleid', 'value'), Input("sub_reset", "n_clicks")])
def return_ngssampleid_value(value, reset_click):
    if reset_click is None:
        return value
    else:
        return def_metadata['sub_ngssampleid']

@app.callback(Output('sub_requestid_final', 'data'), [Input('sub_requestid', 'value'), Input("sub_reset", "n_clicks")])
def return_requestid_value(value, reset_click):
    if reset_click is None:
        return value
    else:
        return def_metadata['sub_requestid']

@app.callback(Output('sub_rawdatapath_final', 'data'), [Input('sub_rawdatapath', 'value'), Input("sub_reset", "n_clicks")])
def return_rawdatapath_value(value, reset_click):
    if reset_click is None:
        return value
    else:
        return def_metadata['sub_rawdatapath']

@app.callback(Output('sub_notes_final', 'data'), [Input('sub_notes', 'value'), Input("sub_reset", "n_clicks")])
def return_notes_value(value, reset_click):
    if reset_click is None:
        return value
    else:
        return def_metadata['sub_notes']


# sub_submitter
# sub_description
# sub_library
# sub_readmode
# sub_flowcellid
# sub_ngssampleid
# sub_requestid
# sub_rawdatapath
# sub_notes
# sub_reset


@du.callback(
    output=Output('callback-submitter', 'children'),
    id='dash-uploader',
)
def get_a_list(filenames):
    return html.Ul([html.Li(filenames)])

@app.callback(
    Output("sub_reset_data", "children"), [Input("sub_reset", "n_clicks")]
)
def on_button_click(n):
    if n is None:
        return "Not clicked." 
    else:
        return f"Clicked {n} times." 

# @app.callback(Output('output','children'),
#              Input('sub_reset','n_clicks'))
# def update(sub_reset):
#     import ipdb; ipdb.set_trace()
#     if not sub_reset or sub_reset == 0:
#         return(1)
#     if sub_reset>0:
#         return(0)
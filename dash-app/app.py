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


app = dash.Dash(external_stylesheets=[dbc.themes.LITERA])


SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
PROJECT_DIR = os.path.join( SCRIPT_DIR, '..' )
DATA_DIR = os.path.join( PROJECT_DIR, 'data/' )
sys.path.append(os.path.normpath(os.path.join(PROJECT_DIR, "app")))



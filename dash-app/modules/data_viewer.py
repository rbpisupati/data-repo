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
from glob import glob

from app import app

def read_data(data_dir):
    all_submissions = glob(data_dir)
    # for ef in 

    return(all_submissions)

layout = html.P("This is the content of the home page!")
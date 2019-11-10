# Run Command
# bokeh serve --show main.py

import pandas as pd

# os methods for manipulating paths
from os.path import dirname, join

# Bokeh basics 
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs

import pandas as pd
import numpy as np

from bokeh.io import show, output_notebook, push_notebook
from bokeh.plotting import figure

from bokeh.models import CategoricalColorMapper, HoverTool, ColumnDataSource, Panel
from bokeh.models.widgets import CheckboxGroup, Slider, RangeSlider, Tabs, FileInput, Button

from bokeh.layouts import column, row, WidgetBox
from bokeh.palettes import Category20_20

from bokeh.application.handlers import FunctionHandler
from bokeh.application import Application

from bokeh.plotting import figure, curdoc

from os.path import dirname, join

import pandas as pd
import numpy as np
import math

from bokeh.io import show, output_notebook, push_notebook
from bokeh.plotting import figure

from bokeh.models import CategoricalColorMapper, HoverTool, ColumnDataSource, Panel, NumeralTickFormatter
from bokeh.models.widgets import CheckboxGroup, Slider, RangeSlider, Tabs

from bokeh.layouts import column, row, WidgetBox
from bokeh.palettes import Category20_20

from bokeh.application.handlers import FunctionHandler
from bokeh.application import Application

from bokeh.plotting import figure, curdoc

from scripts.category_wise_reviews import category_wise_reviews_tab
from scripts.most_reviewed_categories import most_reviewed_categories_tab
from scripts.product_reviews_over_time import product_reviews_over_time_tab

import base64
import io

dataset = pd.read_csv('myapp/dataset/CDs_and_Vinyl_5.csv', skipinitialspace=True)
dataset.columns = ['asin', 'reviewerID', 'overall', 'unixReviewTime']
metadata = pd.read_csv('myapp/dataset/CDs_And_Vinyl_meta_5.csv', skipinitialspace=True)
metadata.columns = ['Product ID', 'Description', 'price', 'Category']

def upload_dataset(attr, old, new):
    global dataset
    dataset = pd.read_csv(io.BytesIO(base64.b64decode(dataset_file_input.value)), skipinitialspace=True)
    dataset.columns = ['asin', 'reviewerID', 'overall', 'unixReviewTime']

dataset_file_input = FileInput(accept=".csv")
dataset_file_input.on_change('value', upload_dataset)

def upload_metadata(attr, old, new):
    global metadata
    metadata = pd.read_csv(io.BytesIO(base64.b64decode(metadata_file_input.value)), skipinitialspace=True)
    metadata.columns = ['Product ID', 'Description', 'price', 'Category']

metadata_file_input = FileInput(accept=".csv")
metadata_file_input.on_change('value', upload_metadata)

def refresh_with_new_data():
    global tab0, home_layout
    updated_tab1 = most_reviewed_categories_tab(dataset, metadata)
    updated_tab2 = product_reviews_over_time_tab(dataset, metadata)
    updated_tab3 = category_wise_reviews_tab(dataset, metadata)
    updated_tabs = Tabs(tabs=[tab0, updated_tab1, updated_tab2, updated_tab3])
    home_layout.children[0] = row(updated_tabs)

upload_button = Button(label="Upload Data", button_type="primary")
upload_button.on_click(refresh_with_new_data)

# Default Home Page

def load_cd_and_vinyl_data():
    global dataset, metadata
    dataset = pd.read_csv('myapp/dataset/CDs_and_Vinyl_5.csv', skipinitialspace=True)
    metadata = pd.read_csv('myapp/dataset/CDs_And_Vinyl_meta_5.csv', skipinitialspace=True)
    refresh_with_new_data()

cd_and_vinyl_data_button = Button(label="Load CD & Vinyl Data", button_type="success")
cd_and_vinyl_data_button.on_click(load_cd_and_vinyl_data)

def load_music_and_instruments_data():
    global dataset, metadata
    dataset = pd.read_csv('myapp/dataset/Musical_Instruments_5.csv', skipinitialspace=True)
    metadata = pd.read_csv('myapp/dataset/Music_Instruments_meta_5.csv', skipinitialspace=True)
    refresh_with_new_data()

music_and_instruments_data_button = Button(label="Load Music & Instruments Data", button_type="success")
music_and_instruments_data_button.on_click(load_music_and_instruments_data)

tab0_layout = column(
    dataset_file_input, metadata_file_input, upload_button,
    row(cd_and_vinyl_data_button, music_and_instruments_data_button))
tab0 = Panel(child=tab0_layout, title='Datasource Selector')

# Create each of the tabs
tab1 = most_reviewed_categories_tab(dataset, metadata)
tab2 = product_reviews_over_time_tab(dataset, metadata)
tab3 = category_wise_reviews_tab(dataset, metadata)

# Put all the tabs into one application
tabs = Tabs(tabs = [tab0, tab1, tab2, tab3])
home_layout = row(tabs)

# Put the tabs in the current document for display
curdoc().add_root(home_layout)

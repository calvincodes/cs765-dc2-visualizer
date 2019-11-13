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
from bokeh.models.widgets import CheckboxGroup, Slider, RangeSlider, Tabs, FileInput, Button, DataTable, TableColumn, PreText

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
from bokeh.models.widgets import CheckboxGroup, Slider, RangeSlider, Tabs, Div

from bokeh.layouts import column, row, WidgetBox
from bokeh.palettes import Category20_20

from bokeh.application.handlers import FunctionHandler
from bokeh.application import Application

from bokeh.plotting import figure, curdoc

from scripts.category_wise_reviews import category_wise_reviews_tab
from scripts.most_reviewed_categories import most_reviewed_categories_tab
from scripts.product_reviews_over_time import product_reviews_over_time_tab
from scripts.product_reviews_over_time_with_slider import product_reviews_over_time_with_slider_tab

import base64
import io

heading_div = Div(text="""<br><h1 style="box-sizing: border-box; margin-top: 0px; margin-bottom: 0.5rem; font-family: &quot;Nunito Sans&quot;, -apple-system, system-ui, &quot;Segoe UI&quot;, Roboto, &quot;Helvetica Neue&quot;, Arial, sans-serif, &quot;Apple Color Emoji&quot;, &quot;Segoe UI Emoji&quot;, &quot;Segoe UI Symbol&quot;; font-weight: 600; color: rgb(26, 26, 26); font-size: 2rem; text-transform: uppercase; letter-spacing: 3px;">DESIGN CHALLENGE 2</h1><pre>Analyze Product Trends. Use sample data or upload custom files. Navigate through tabs for different visualizations.</pre><hr>""", width=1000, height=120, style={'text-align':'center'})
footer_div = Div(text="""<font color="black" size="3"><a href="https://github.com/calvincodes/cs765-dc2-visualizer" target="_blank">Github Link</a></font>""", width=1000, height=20, style={'text-align':'center'})

dataset = pd.read_csv('myapp/dataset/Musical_Instruments_5.csv', skipinitialspace=True)
dataset.columns = ['asin', 'reviewerID', 'overall', 'unixReviewTime']
metadata = pd.read_csv('myapp/dataset/Music_Instruments_meta_5.csv', skipinitialspace=True)
metadata.columns = ['Product ID', 'Description', 'price', 'Category']

def upload_dataset(attr, old, new):
    global dataset
    dataset = pd.read_csv(io.BytesIO(base64.b64decode(dataset_file_input.value)), skipinitialspace=True)
    dataset.columns = ['asin', 'reviewerID', 'overall', 'unixReviewTime']

pre_dataset = PreText(text="""Reviews Dataset CSV File""",width=200, height=10)
dataset_file_input = FileInput(accept=".csv")
dataset_file_input.on_change('value', upload_dataset)

def upload_metadata(attr, old, new):
    global metadata
    metadata = pd.read_csv(io.BytesIO(base64.b64decode(metadata_file_input.value)), skipinitialspace=True)
    metadata.columns = ['Product ID', 'Description', 'price', 'Category']

pre_metadata = PreText(text="""Metadata CSV File""",width=150, height=10)
metadata_file_input = FileInput(accept=".csv")
metadata_file_input.on_change('value', upload_metadata)

current_dataset = "Music & Instrument Data"

current_dataset_div = Div(text="<h2><mark>\""+current_dataset+"\"</mark> Loaded!</h2>", width=1000, height=50, style={'text-align':'center'})

def get_data_analytics():
    combined_data = dataset.set_index('asin').join(metadata.set_index('Product ID')).reset_index()
    combined_data.columns = ['asin', 'reviewerID', 'overall', 'unixReviewTime', 'Description', 'price', 'Category']

    unique_products = combined_data['asin'].nunique()
    unique_category = combined_data['Category'].nunique()
    total_reviews = len(combined_data)
    unique_reviewers = combined_data['reviewerID'].nunique()

    data_analytics = dict(
        attr=['Total Products', 'Total Categories', 'Total Reviews', 'Unique Reviewers'],
        vals=[unique_products, unique_category, total_reviews, unique_reviewers]
    )
    return data_analytics


analytics_source = ColumnDataSource(get_data_analytics())

analytics_columns = [
    TableColumn(field="attr", title="Attributes"),
    TableColumn(field="vals", title="Values"),
]
analytics_table = DataTable(source=analytics_source, columns=analytics_columns, width=1000, height=150)

def refresh_with_new_data(dataset_enum):
    global tab0, tab3, home_layout, current_dataset

    if dataset_enum == 1:
        current_dataset = "CD & Vinyl Data"
    if dataset_enum == 2:
        current_dataset = "Music & Instrument Data"
    if dataset_enum == 3:
        current_dataset = "User Provided Data"

    analytics_source.data = get_data_analytics()

    updated_tab1 = product_reviews_over_time_tab(dataset, metadata)
    updated_tab2 = most_reviewed_categories_tab(dataset, metadata)
    # updated_tab4 = category_wise_reviews_tab(dataset, metadata)
    updated_tabs = Tabs(tabs=[tab0, updated_tab1, updated_tab2, tab3])
    current_dataset_div.text = "<h2><mark>\""+current_dataset+"\"</mark> Loaded!</h2>"
    home_layout.children[0] = row(updated_tabs)

def button_click_handler():
    current_dataset_div.text = "<h2>Loading ........</h2>"
    refresh_with_new_data(3)

upload_button = Button(label="Upload Data", button_type="primary")
upload_button.on_click(button_click_handler)

# Default Home Page

def load_cd_and_vinyl_data():
    current_dataset_div.text = "<h2>Loading ........</h2>"
    global dataset, metadata
    dataset = pd.read_csv('myapp/dataset/CDs_and_Vinyl_5.csv', skipinitialspace=True)
    metadata = pd.read_csv('myapp/dataset/CDs_And_Vinyl_meta_5.csv', skipinitialspace=True)
    refresh_with_new_data(1)

cd_and_vinyl_data_button = Button(label="Load CD & Vinyl Data", button_type="success", width=500)
cd_and_vinyl_data_button.on_click(load_cd_and_vinyl_data)

def load_music_and_instruments_data():
    current_dataset_div.text = "<h2>Loading ........</h2>"
    global dataset, metadata
    dataset = pd.read_csv('myapp/dataset/Musical_Instruments_5.csv', skipinitialspace=True)
    metadata = pd.read_csv('myapp/dataset/Music_Instruments_meta_5.csv', skipinitialspace=True)
    refresh_with_new_data(2)

music_and_instruments_data_button = Button(label="Load Music & Instruments Data", button_type="success", width=500)
music_and_instruments_data_button.on_click(load_music_and_instruments_data)

sample_data_div = Div(text="""<font color="black"><a href="https://github.com/calvincodes/cs765-dc2-visualizer/tree/master/myapp/dataset/synthetic%20data%20sets" target="_blank"><b>Click here</b></a> for input file format details and sample input files.</font>""", width=1000, height=20, style={'text-align':'center'})

tab0_layout = column(heading_div,
    row(pre_dataset, dataset_file_input),
    row(pre_metadata, metadata_file_input),
    sample_data_div,
    upload_button,
    row(cd_and_vinyl_data_button, music_and_instruments_data_button),
    current_dataset_div,
    analytics_table,
    footer_div)
tab0 = Panel(child=tab0_layout, title='Datasource Selector')

# Create each of the tabs
tab1 = product_reviews_over_time_tab(dataset, metadata)
tab2 = most_reviewed_categories_tab(dataset, metadata)
tab3 = product_reviews_over_time_with_slider_tab(dataset, metadata)
# tab4 = category_wise_reviews_tab(dataset, metadata)

# Put all the tabs into one application
tabs = Tabs(tabs = [tab0, tab1, tab2, tab3])
home_layout = row(tabs)

# Put the tabs in the current document for display
curdoc().add_root(home_layout)

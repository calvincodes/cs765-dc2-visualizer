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
from bokeh.models.widgets import CheckboxGroup, Slider, RangeSlider, Tabs

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

# dataset = pd.read_csv(join(dirname(__file__), 'dataset', 'CDs_and_Vinyl_5.csv'), skipinitialspace=True)
# metadata = pd.read_csv(join(dirname(__file__), 'dataset', 'CDs_And_Vinyl_meta_5.csv'), skipinitialspace=True)

dataset = pd.read_csv('myapp/dataset/CDs_and_Vinyl_5.csv', skipinitialspace=True)
metadata = pd.read_csv('myapp/dataset/CDs_And_Vinyl_meta_5.csv', skipinitialspace=True)

# Create each of the tabs
tab1 = category_wise_reviews_tab(dataset, metadata)
tab2 = most_reviewed_categories_tab(dataset, metadata)

# Put all the tabs into one application
tabs = Tabs(tabs = [tab1, tab2])

# Put the tabs in the current document for display
curdoc().add_root(tabs)

# Run Command
# bokeh serve --show main.py

import pandas as pd

# os methods for manipulating paths
from os.path import dirname, join

# Bokeh basics 
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs


# Each tab is drawn by one script
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

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


def category_wise_reviews_tab(cd_and_vinyl, cd_and_vinyl_meta):

    # cd_and_vinyl = pd.read_csv('../dataset/CDs_and_Vinyl_5.csv', skipinitialspace=True)
    # cd_and_vinyl_meta = pd.read_csv('../dataset/CDs_And_Vinyl_meta_5.csv', skipinitialspace=True)
    # cd_and_vinyl = pd.read_csv(join(dirname(__file__), 'dataset', 'CDs_and_Vinyl_5.csv'), skipinitialspace=True)
    # cd_and_vinyl_meta = pd.read_csv(join(dirname(__file__), 'dataset', 'CDs_And_Vinyl_meta_5.csv'), skipinitialspace=True)

    combined_data = cd_and_vinyl.set_index('asin').join(cd_and_vinyl_meta.set_index('Product ID'))
    category_to_avg_rating_list = combined_data.groupby('Category', as_index=False)['overall'].mean()

    def make_dataset(category_list):
        return category_to_avg_rating_list[category_to_avg_rating_list['Category'].isin(category_list)]

    category_selection = CheckboxGroup(labels=category_to_avg_rating_list.Category.unique().tolist(),
                                       active=[0, 1])
    initial_categories = [category_selection.labels[i] for i in category_selection.active]
    src = make_dataset(initial_categories)

    p = figure(x_range=initial_categories, y_range=(1,6), plot_height=700, plot_width = 1000, title="Category Wise Reviews")
    p.xgrid.grid_line_color = None
    p.y_range.start = 0

    r = p.vbar(x=initial_categories, top=src.overall.tolist(), width=0.1)
    ds = r.data_source

    def update(attr, old, new):

        # Get the list of carriers for the graph
        categories_to_plot = [category_selection.labels[i] for i in
                            category_selection.active]
        # Make a new dataset based on the selected carriers and the
        # make_dataset function defined earlier
        new_src = make_dataset(categories_to_plot)
        # Update the source used in the quad glpyhs
        # src.data.update(new_src.data)
        new_data = dict()
        new_data['x_range'] = new_src.Category.unique().tolist()
        new_data['x'] = new_src.Category.unique().tolist()
        new_data['top'] = new_src.overall.tolist()

        p.x_range.factors = new_data['x_range']

        ds.data = new_data

    category_selection.on_change('active', update)
    controls = WidgetBox(category_selection)

    layout = row(controls, p)
    # curdoc().add_root(layout)

    tab = Panel(child=layout, title='Category Wise Reviews')
    return tab


def getKColors(k):
    k_color_list = []
    for i in range(k):
        k_color_list.append(Category20_20[i % 20])

    return k_color_list

def most_reviewed_categories_tab(dataset, metadata):

    # dataset = pd.read_csv('../dataset/CDs_and_Vinyl_5.csv', skipinitialspace=True)
    # metadata = pd.read_csv('../dataset/CDs_And_Vinyl_meta_5.csv', skipinitialspace=True)
    # dataset = pd.read_csv(join(dirname(__file__), 'dataset', 'CDs_and_Vinyl_5.csv'), skipinitialspace=True)
    # metadata = pd.read_csv(join(dirname(__file__), 'dataset', 'CDs_and_Vinyl_5.csv'), skipinitialspace=True)

    combined_data = dataset.set_index('asin').join(metadata.set_index('Product ID'))

    category_to_mean_and_total_reviews = combined_data.groupby('Category')['overall'].agg(['mean', 'count']).reset_index()
    category_to_mean_and_total_reviews.columns = ['Category', 'average', 'total']

    category_count = category_to_mean_and_total_reviews.shape[0]
    category_to_mean_and_total_reviews = category_to_mean_and_total_reviews.sort_values('total', ascending=False)

    default = 10
    plot_data = category_to_mean_and_total_reviews.head(default)
    source = ColumnDataSource(
        data=dict(
            category=plot_data.Category.tolist(),
            total=plot_data.total.tolist(),
            average=plot_data.average.tolist(),
            color=getKColors(default)))

    p = figure(x_range=plot_data.Category.tolist(), plot_width=1200, plot_height=700)
    r = p.vbar(source=source, x='category', width=0.4, bottom=0,
           top='total', color='color')

    # Adding hover tool
    hover = HoverTool(tooltips=[('Category', '@category'),
                                ('Avg Review', '@average'),
                                ('Total Reviews', '@total')],
                      mode='vline')
    p.add_tools(hover)

    # Formatting axes
    p.xaxis.axis_label = "Category"
    p.xaxis.major_label_orientation = math.pi/2
    p.xaxis.major_label_text_font_size = "10pt"
    p.xaxis.axis_label_text_font_size = "15pt"

    p.yaxis.axis_label = "Total Reviews"
    p.yaxis.formatter=NumeralTickFormatter(format="0")
    p.yaxis.major_label_text_font_size = "10pt"
    p.yaxis.axis_label_text_font_size = "15pt"

    ds = r.data_source

    top_k_select_slider = Slider(start = 1, end = category_count,
                                 step = 5, value = default,
                                 title = 'Top k Categories')

    def update(attr, old, new):

        new_count = top_k_select_slider.value
        new_plot_data = category_to_mean_and_total_reviews.head(new_count)
        new_colors = getKColors(new_count)

        new_data = dict()
        new_data['x_range'] = new_plot_data.Category.tolist()
        new_data['category'] = new_plot_data.Category.tolist()
        new_data['average'] = new_plot_data.average.tolist()
        new_data['total'] = new_plot_data.total.tolist()
        new_data['color'] = new_colors

        p.x_range.factors = new_data['x_range']

        ds.data = new_data

    top_k_select_slider.on_change('value', update)

    layout = column(top_k_select_slider, p)
    # curdoc().add_root(layout)

    tab = Panel(child=layout, title='Most Reviewed Categories')
    return tab

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

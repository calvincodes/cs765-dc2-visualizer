# Run Command
# bokeh serve --show category-wise-reviews.py

from os.path import dirname, join

import pandas as pd
import numpy as np

from bokeh.io import show, output_notebook, push_notebook
from bokeh.plotting import figure

from bokeh.models import CategoricalColorMapper, HoverTool, ColumnDataSource, Panel
from bokeh.models.widgets import CheckboxGroup, Slider, RangeSlider, Tabs

from bokeh.layouts import column, row, WidgetBox
from bokeh.palettes import Category20_16

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

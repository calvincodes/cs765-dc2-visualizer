# Run Command
# bokeh serve --show category-wise-reviews.py

from os.path import dirname, join

import pandas as pd
import numpy as np

from bokeh.io import show, output_notebook, push_notebook
from bokeh.plotting import figure

from bokeh.models import CategoricalColorMapper, HoverTool, ColumnDataSource, Panel
from bokeh.models.widgets import CheckboxGroup, Slider, RangeSlider, Tabs, FileInput

from bokeh.layouts import column, row, WidgetBox
from bokeh.palettes import Category20_16

from bokeh.application.handlers import FunctionHandler
from bokeh.application import Application

from bokeh.plotting import figure, curdoc

from .helper import getKColors

def category_wise_reviews_tab(cd_and_vinyl, cd_and_vinyl_meta):

    combined_data = cd_and_vinyl.set_index('asin').join(cd_and_vinyl_meta.set_index('Product ID'))
    category_to_avg_rating_list = combined_data.groupby('Category', as_index=False)['overall'].mean()
    category_to_avg_rating_list.columns = ['category', 'average']

    category_selection = CheckboxGroup(
        labels=category_to_avg_rating_list.category.unique().tolist(),
        active=[0, 1, 2, 3])

    initial_categories = [category_selection.labels[i] for i in category_selection.active]
    plot_data = category_to_avg_rating_list[category_to_avg_rating_list['category'].isin(initial_categories)]

    source = ColumnDataSource(
        data=dict(
            category=plot_data.category.tolist(),
            average=plot_data.average.tolist(),
            color=getKColors(len(plot_data.category.tolist()))))

    p = figure(x_range=plot_data.category.tolist(), y_range=(1, 6), plot_height=700, plot_width=1000,
               title="Category Wise Reviews")
    p.xgrid.grid_line_color = None
    p.y_range.start = 0

    r = p.vbar(source=source, x='category', top='average', color='color', width=0.1)
    ds = r.data_source

    def update_plot(attr, old, new):

        categories_to_plot = [category_selection.labels[i] for i in category_selection.active]

        new_plot_data = category_to_avg_rating_list[category_to_avg_rating_list['category'].isin(categories_to_plot)]

        new_data = dict()
        new_colors = getKColors(len(new_plot_data.category.tolist()))
        new_data['x_range'] = new_plot_data.category.tolist()
        new_data['category'] = new_plot_data.category.tolist()
        new_data['average'] = new_plot_data.average.tolist()
        new_data['color'] = new_colors

        p.x_range.factors = new_data['x_range']

        ds.data = new_data

    category_selection.on_change('active', update_plot)
    controls = WidgetBox(category_selection)

    layout = row(controls, p)
    tab = Panel(child=layout, title='Category Wise Reviews')
    return tab

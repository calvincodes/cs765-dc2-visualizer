# Run Command
# bokeh serve --show most-reviewed-categories.py

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

from .helper import getKColors

def most_reviewed_categories_tab(dataset, metadata):

    heading_div = Div(text="""<br><h3 style="box-sizing: border-box; margin-top: 0px; margin-bottom: 0.5rem; font-family: &quot;Nunito Sans&quot;, -apple-system, system-ui, &quot;Segoe UI&quot;, Roboto, &quot;Helvetica Neue&quot;, Arial, sans-serif, &quot;Apple Color Emoji&quot;, &quot;Segoe UI Emoji&quot;, &quot;Segoe UI Symbol&quot;; font-weight: 600; color: rgb(26, 26, 26); font-size: 2rem; text-transform: uppercase; letter-spacing: 3px;">Top k Categories</h3><pre>Slide to select k.</pre><hr>""",
        width=1000, height=120, style={'text-align': 'center'})

    combined_data = dataset.set_index('asin').join(metadata.set_index('Product ID'))

    category_to_mean_and_total_reviews = combined_data.groupby('Category')['overall'].agg(['mean', 'count']).reset_index()
    category_to_mean_and_total_reviews.columns = ['Category', 'average', 'total']

    category_count = category_to_mean_and_total_reviews.shape[0]
    category_to_mean_and_total_reviews = category_to_mean_and_total_reviews.sort_values('total', ascending=False)

    default = 10 if category_count > 10 else category_count
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
                                 title = 'Top k Categories', bar_color="red")

    def update_plot(attr, old, new):

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

    top_k_select_slider.on_change('value', update_plot)

    layout = column(heading_div, top_k_select_slider, p)
    tab = Panel(child=layout, title='Most Reviewed Categories')
    return tab

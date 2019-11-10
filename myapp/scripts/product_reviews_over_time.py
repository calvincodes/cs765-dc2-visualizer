from os.path import dirname, join

import pandas as pd
import numpy as np
import math

from bokeh.io import show, output_notebook, push_notebook
from bokeh.plotting import figure

from bokeh.models import CategoricalColorMapper, HoverTool, ColumnDataSource, Panel, NumeralTickFormatter
from bokeh.models.widgets import CheckboxGroup, Slider, RangeSlider, Tabs, RadioButtonGroup, Select

from bokeh.layouts import column, row, WidgetBox
from bokeh.palettes import Category20_20

from bokeh.application.handlers import FunctionHandler
from bokeh.application import Application

from bokeh.plotting import figure, curdoc

from .helper import getKColors

def product_reviews_over_time_tab(dataset, metadata):

    combined_data = dataset.set_index('asin').join(metadata.set_index('Product ID')).reset_index()
    combined_data.columns = ['asin', 'reviewerID', 'overall', 'unixReviewTime', 'Description', 'price', 'Category']

    # Default selected_product is the most_purchased_product
    selected_product = combined_data.asin.value_counts().head(1).index[0]
    filtered_data = combined_data[combined_data['asin'] == selected_product]

    filtered_data['dtReviewTime'] = pd.to_datetime(filtered_data['unixReviewTime'], unit='s')
    filtered_data['reviewYear'] = filtered_data['dtReviewTime'].dt.strftime('%Y')
    filtered_data['reviewMonth'] = filtered_data['dtReviewTime'].dt.strftime('%Y-%m')
    filtered_data['dtReviewTime'] = filtered_data['dtReviewTime'].dt.strftime('%Y-%m-%d')
    filtered_data = filtered_data.sort_values('dtReviewTime')

    year_wise_reviews = filtered_data.groupby('reviewYear')['overall'].agg(['mean', 'count']).reset_index()
    year_wise_reviews.columns = ['time', 'average', 'total']

    month_wise_reviews = filtered_data.groupby('reviewMonth')['overall'].agg(['mean', 'count']).reset_index()
    month_wise_reviews.columns = ['time', 'average', 'total']

    date_wise_reviews = filtered_data.groupby('dtReviewTime')['overall'].agg(['mean', 'count']).reset_index()
    date_wise_reviews.columns = ['time', 'average', 'total']

    # Default plot is Year Wise Reviews
    plot_data = year_wise_reviews
    source = ColumnDataSource(
        data=dict(
            time_stamp=list(map(str, plot_data['time'])),
            total=plot_data.total.tolist(),
            average=plot_data.average.tolist(),
            color=getKColors(len(plot_data))))

    # Adding hover tool
    hover = HoverTool(tooltips=[('Time', '@time_stamp'),
                                ('Avg Review', '@average'),
                                ('Total Reviews', '@total')],
                      mode='vline')

    # Total Reviews Figure
    p1 = figure(x_range=plot_data.time.tolist(), plot_width=1200, plot_height=300)
    r1 = p1.line(source=source, x='time_stamp', y='total', line_width=2)

    p1.add_tools(hover)

    # Formatting axes
    p1.xaxis.axis_label = "Time"
    p1.xaxis.major_label_orientation = math.pi / 2
    p1.xaxis.major_label_text_font_size = "10pt"
    p1.xaxis.axis_label_text_font_size = "15pt"

    p1.yaxis.axis_label = "Total Reviews"
    p1.yaxis.formatter = NumeralTickFormatter(format="0")
    p1.yaxis.major_label_text_font_size = "10pt"
    p1.yaxis.axis_label_text_font_size = "15pt"

    ds1 = r1.data_source

    # Average Review Figure
    p2 = figure(x_range=plot_data.time.tolist(), plot_width=1200, plot_height=300)
    r2 = p2.line(source=source, x='time_stamp', y='average', line_width=2)

    p2.add_tools(hover)

    # Formatting axes
    p2.xaxis.axis_label = "Time"
    p2.xaxis.major_label_orientation = math.pi / 2
    p2.xaxis.major_label_text_font_size = "10pt"
    p2.xaxis.axis_label_text_font_size = "15pt"

    p2.yaxis.axis_label = "Average Review"
    p2.yaxis.formatter = NumeralTickFormatter(format="0")
    p2.yaxis.major_label_text_font_size = "10pt"
    p2.yaxis.axis_label_text_font_size = "15pt"

    ds2 = r2.data_source

    radio_button_group = RadioButtonGroup(
        labels=["Yearly", "Monthly", "Daily"], active=0)

    def update_plot(attr, old, new):

        new_plot_data = plot_data

        if radio_button_group.active == 0:
            new_plot_data = year_wise_reviews
        if radio_button_group.active == 1:
            new_plot_data = month_wise_reviews
        if radio_button_group.active == 2:
            new_plot_data = date_wise_reviews

        new_colors = getKColors(len(new_plot_data))

        new_data = dict()
        new_data['x_range'] = new_plot_data.time.tolist()
        new_data['time_stamp'] = new_plot_data.time.tolist()
        new_data['average'] = new_plot_data.average.tolist()
        new_data['total'] = new_plot_data.total.tolist()
        new_data['color'] = new_colors

        p1.x_range.factors = new_data['x_range']
        p2.x_range.factors = new_data['x_range']

        ds1.data = new_data
        ds2.data = new_data

    radio_button_group.on_change('active', update_plot)

    def update_selection(attr, old, new):
        #TODO: Implement this
        return

    # select_product = Select(title="Product Id:", value=selected_product, options=combined_data['asin'].unique().tolist())
    # select_product.on_change('value', update_selection)

    # layout = column(select_product, radio_button_group, p1, p2)
    layout = column(radio_button_group, p1, p2)
    tab = Panel(child=layout, title='Product Reviews Over Time')
    return tab
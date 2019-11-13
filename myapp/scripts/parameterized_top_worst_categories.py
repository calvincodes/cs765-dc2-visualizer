# Run Command
# bokeh serve --show most-reviewed-categories.py

from os.path import dirname, join

import pandas as pd
import numpy as np
import math

from bokeh.io import show, output_notebook, push_notebook
from bokeh.plotting import figure

from bokeh.models import CategoricalColorMapper, HoverTool, ColumnDataSource, Panel, NumeralTickFormatter, LabelSet
from bokeh.models.widgets import CheckboxGroup, Slider, RangeSlider, Tabs, Div, TextInput, Button

from bokeh.layouts import column, row, WidgetBox
from bokeh.palettes import Category20_20

from bokeh.application.handlers import FunctionHandler
from bokeh.application import Application

from bokeh.plotting import figure, curdoc

from .helper import getKColors

def parameterized_top_worst_categories_tab(dataset, metadata):

    heading_div = Div(text="""<br><h3 style="box-sizing: border-box; margin-top: 0px; margin-bottom: 0.5rem; font-family: &quot;Nunito Sans&quot;, -apple-system, system-ui, &quot;Segoe UI&quot;, Roboto, &quot;Helvetica Neue&quot;, Arial, sans-serif, &quot;Apple Color Emoji&quot;, &quot;Segoe UI Emoji&quot;, &quot;Segoe UI Symbol&quot;; font-weight: 600; color: rgb(26, 26, 26); font-size: 2rem; text-transform: uppercase; letter-spacing: 3px;">Top k Categories</h3><pre>Slide to select k.</pre><hr>""",
        width=1000, height=120, style={'text-align': 'center'})

    combined_data = dataset.set_index('asin').join(metadata.set_index('Product ID'))

    category_to_mean_and_total_reviews = combined_data.groupby('Category')['overall'].agg(['mean', 'count']).reset_index()
    category_to_mean_and_total_reviews.columns = ['Category', 'average', 'total']

    top_performers = category_to_mean_and_total_reviews[
        (category_to_mean_and_total_reviews['average'] > 4.5) & (category_to_mean_and_total_reviews['total'] > 300)]
    worst_performers = category_to_mean_and_total_reviews[
        (category_to_mean_and_total_reviews['average'] < 3.5) & (category_to_mean_and_total_reviews['total'] > 10)]

    best_performing_rating_text = TextInput(value="4.5", title="Avg Rating More Than:")
    best_performing_total_text = TextInput(value="300", title="Total Reviews More Than:")
    best_performing_button = Button(label="Search Top Performers", button_type="success", width=600)

    worst_performing_rating_text = TextInput(value="3.5", title="Avg Rating Less Than:")
    worst_performing_total_text = TextInput(value="10", title="Total Reviews More Than:")
    worst_performing_button = Button(label="Search Worst Performers", button_type="danger", width=600)

    category_count = category_to_mean_and_total_reviews.shape[0]
    top_category_by_total_reviews = category_to_mean_and_total_reviews.sort_values('total', ascending=False)
    bottom_category_by_total_reviews = top_category_by_total_reviews[::-1]
    top_category_by_avg_reviews = category_to_mean_and_total_reviews.sort_values('average', ascending=False)
    bottom_category_by_avg_reviews = top_category_by_avg_reviews[::-1]

    default = 10 if category_count > 10 else category_count

    # top_k_by_total_reviews_plot_data = top_category_by_total_reviews.head(default)
    top_k_by_total_reviews_plot_data = top_performers
    top_k_by_total_reviews_source = ColumnDataSource(
        data=dict(
            category=top_k_by_total_reviews_plot_data.Category.tolist(),
            total=top_k_by_total_reviews_plot_data.total.tolist(),
            average=top_k_by_total_reviews_plot_data.average.tolist(),
            color=getKColors(len(top_k_by_total_reviews_plot_data))))

    p_top_k_by_total_reviews = figure(title="Top Performers by Total Reviews", x_range=top_k_by_total_reviews_plot_data.Category.tolist(), plot_width=700, plot_height=400)
    r_top_k_by_total_reviews = p_top_k_by_total_reviews.vbar(source=top_k_by_total_reviews_source, x='category', width=0.4, bottom=0,
           top='total', color='color')

    # Adding hover tool
    hover = HoverTool(tooltips=[('Category', '@category'),
                                ('Avg Review', '@average'),
                                ('Total Reviews', '@total')],
                      mode='vline')
    p_top_k_by_total_reviews.add_tools(hover)

    # Formatting axes
    p_top_k_by_total_reviews.xaxis.axis_label = ''
    p_top_k_by_total_reviews.xaxis.major_label_orientation = math.pi/2
    p_top_k_by_total_reviews.xaxis.major_label_text_font_size = "10pt"
    p_top_k_by_total_reviews.xaxis.axis_label_text_font_size = "0pt"

    p_top_k_by_total_reviews.yaxis.axis_label = "Total Reviews"
    p_top_k_by_total_reviews.yaxis.formatter=NumeralTickFormatter(format="0")
    p_top_k_by_total_reviews.yaxis.major_label_text_font_size = "10pt"
    p_top_k_by_total_reviews.yaxis.axis_label_text_font_size = "15pt"

    ds_top_k_by_total_reviews = r_top_k_by_total_reviews.data_source

    # bottom_k_by_total_reviews_plot_data = bottom_category_by_total_reviews.head(default)
    bottom_k_by_total_reviews_plot_data = worst_performers
    bottom_k_by_total_reviews_plot_source = ColumnDataSource(
        data=dict(
            category=bottom_k_by_total_reviews_plot_data.Category.tolist(),
            total=bottom_k_by_total_reviews_plot_data.total.tolist(),
            average=bottom_k_by_total_reviews_plot_data.average.tolist(),
            color=getKColors(len(bottom_k_by_total_reviews_plot_data))))

    p_bottom_k_by_total_reviews = figure(title="Worst Performers by Total Reviews", x_range=bottom_k_by_total_reviews_plot_data.Category.tolist(), plot_width=700, plot_height=400)
    r_bottom_k_by_total_reviews = p_bottom_k_by_total_reviews.vbar(source=bottom_k_by_total_reviews_plot_source, x='category', width=0.4, bottom=0,
                           top='total', color='color')
    p_bottom_k_by_total_reviews.add_tools(hover)

    # Formatting axes
    p_bottom_k_by_total_reviews.xaxis.axis_label = ""
    p_bottom_k_by_total_reviews.xaxis.major_label_orientation = math.pi / 2
    p_bottom_k_by_total_reviews.xaxis.major_label_text_font_size = "10pt"
    p_bottom_k_by_total_reviews.xaxis.axis_label_text_font_size = "0pt"

    p_bottom_k_by_total_reviews.yaxis.axis_label = "Total Reviews"
    p_bottom_k_by_total_reviews.yaxis.formatter = NumeralTickFormatter(format="0")
    p_bottom_k_by_total_reviews.yaxis.major_label_text_font_size = "10pt"
    p_bottom_k_by_total_reviews.yaxis.axis_label_text_font_size = "15pt"

    ds_bottom_k_by_total_reviews = r_bottom_k_by_total_reviews.data_source

    # top_k_by_avg_reviews_plot_data = top_category_by_avg_reviews.head(default)
    top_k_by_avg_reviews_plot_data = top_performers
    top_k_by_avg_reviews_source = ColumnDataSource(
        data=dict(
            category=top_k_by_avg_reviews_plot_data.Category.tolist(),
            total=top_k_by_avg_reviews_plot_data.total.tolist(),
            average=top_k_by_avg_reviews_plot_data.average.tolist(),
            color=getKColors(len(top_k_by_avg_reviews_plot_data))))

    p_top_k_by_avg_reviews = figure(title="Top Performers by Avg Rating",
                                    x_range=top_k_by_avg_reviews_plot_data.Category.tolist(), plot_width=700,
                                    plot_height=400)
    r_top_k_by_avg_reviews = p_top_k_by_avg_reviews.vbar(source=top_k_by_avg_reviews_source, x='category', width=0.4,
                                                         bottom=0,
                                                         top='average', color='color')

    # Adding hover tool
    hover = HoverTool(tooltips=[('Category', '@category'),
                                ('Avg Review', '@average'),
                                ('Total Reviews', '@total')],
                      mode='vline')
    p_top_k_by_avg_reviews.add_tools(hover)

    # Formatting axes
    p_top_k_by_avg_reviews.xaxis.axis_label = "Category"
    p_top_k_by_avg_reviews.xaxis.major_label_orientation = math.pi / 2
    p_top_k_by_avg_reviews.xaxis.major_label_text_font_size = "10pt"
    p_top_k_by_avg_reviews.xaxis.axis_label_text_font_size = "15pt"

    p_top_k_by_avg_reviews.yaxis.axis_label = "Avg Rating"
    p_top_k_by_avg_reviews.yaxis.formatter = NumeralTickFormatter(format="0")
    p_top_k_by_avg_reviews.yaxis.major_label_text_font_size = "10pt"
    p_top_k_by_avg_reviews.yaxis.axis_label_text_font_size = "15pt"

    ds_top_k_by_avg_reviews = r_top_k_by_avg_reviews.data_source

    # bottom_k_by_avg_reviews_plot_data = bottom_category_by_avg_reviews.head(default)
    bottom_k_by_avg_reviews_plot_data = worst_performers
    bottom_k_by_avg_reviews_plot_source = ColumnDataSource(
        data=dict(
            category=bottom_k_by_avg_reviews_plot_data.Category.tolist(),
            total=bottom_k_by_avg_reviews_plot_data.total.tolist(),
            average=bottom_k_by_avg_reviews_plot_data.average.tolist(),
            color=getKColors(len(bottom_k_by_avg_reviews_plot_data))))

    p_bottom_k_by_avg_reviews = figure(title="Worst Performers by Avg Rating",
                                       x_range=bottom_k_by_avg_reviews_plot_data.Category.tolist(), plot_width=700,
                                       plot_height=400)
    r_bottom_k_by_avg_reviews = p_bottom_k_by_avg_reviews.vbar(source=bottom_k_by_avg_reviews_plot_source, x='category',
                                                               width=0.4, bottom=0,
                                                               top='average', color='color')
    p_bottom_k_by_avg_reviews.add_tools(hover)

    # Formatting axes
    p_bottom_k_by_avg_reviews.xaxis.axis_label = "Category"
    p_bottom_k_by_avg_reviews.xaxis.major_label_orientation = math.pi / 2
    p_bottom_k_by_avg_reviews.xaxis.major_label_text_font_size = "10pt"
    p_bottom_k_by_avg_reviews.xaxis.axis_label_text_font_size = "15pt"

    p_bottom_k_by_avg_reviews.yaxis.axis_label = "Avg Rating"
    p_bottom_k_by_avg_reviews.yaxis.formatter = NumeralTickFormatter(format="0")
    p_bottom_k_by_avg_reviews.yaxis.major_label_text_font_size = "10pt"
    p_bottom_k_by_avg_reviews.yaxis.axis_label_text_font_size = "15pt"

    ds_bottom_k_by_avg_reviews = r_bottom_k_by_avg_reviews.data_source

    def update_best_performers():

        if not best_performing_rating_text.value:
            return

        if not best_performing_total_text.value:
            return

        new_top_total_reviews_plot_data = category_to_mean_and_total_reviews[
            (category_to_mean_and_total_reviews['average'] > float(best_performing_rating_text.value))
            & (category_to_mean_and_total_reviews['total'] > int(best_performing_total_text.value))]
        new_top_avg_reviews_plot_data = new_top_total_reviews_plot_data
        new_colors = getKColors(len(new_top_total_reviews_plot_data))

        new_top_by_total_review_data = dict()
        new_top_by_total_review_data['x_range'] = new_top_total_reviews_plot_data.Category.tolist()
        new_top_by_total_review_data['category'] = new_top_total_reviews_plot_data.Category.tolist()
        new_top_by_total_review_data['average'] = new_top_total_reviews_plot_data.average.tolist()
        new_top_by_total_review_data['total'] = new_top_total_reviews_plot_data.total.tolist()
        new_top_by_total_review_data['color'] = new_colors

        new_top_by_avg_review_data = dict()
        new_top_by_avg_review_data['x_range'] = new_top_avg_reviews_plot_data.Category.tolist()
        new_top_by_avg_review_data['category'] = new_top_avg_reviews_plot_data.Category.tolist()
        new_top_by_avg_review_data['average'] = new_top_avg_reviews_plot_data.average.tolist()
        new_top_by_avg_review_data['total'] = new_top_avg_reviews_plot_data.total.tolist()
        new_top_by_avg_review_data['color'] = new_colors

        p_top_k_by_total_reviews.x_range.factors = new_top_by_total_review_data['x_range']
        p_top_k_by_avg_reviews.x_range.factors = new_top_by_avg_review_data['x_range']

        ds_top_k_by_total_reviews.data = new_top_by_total_review_data
        ds_top_k_by_avg_reviews.data = new_top_by_avg_review_data

    def update_worst_performers():

        if not worst_performing_rating_text.value:
            return

        if not worst_performing_total_text.value:
            return

        new_bottom_total_reviews_plot_data = category_to_mean_and_total_reviews[
            (category_to_mean_and_total_reviews['average'] < float(worst_performing_rating_text.value))
            & (category_to_mean_and_total_reviews['total'] > int(worst_performing_total_text.value))]
        new_bottom_avg_reviews_plot_data = new_bottom_total_reviews_plot_data
        new_colors = getKColors(len(new_bottom_total_reviews_plot_data))

        new_bottom_by_total_review_data = dict()
        new_bottom_by_total_review_data['x_range'] = new_bottom_total_reviews_plot_data.Category.tolist()
        new_bottom_by_total_review_data['category'] = new_bottom_total_reviews_plot_data.Category.tolist()
        new_bottom_by_total_review_data['average'] = new_bottom_total_reviews_plot_data.average.tolist()
        new_bottom_by_total_review_data['total'] = new_bottom_total_reviews_plot_data.total.tolist()
        new_bottom_by_total_review_data['color'] = new_colors

        new_bottom_by_avg_review_data = dict()
        new_bottom_by_avg_review_data['x_range'] = new_bottom_avg_reviews_plot_data.Category.tolist()
        new_bottom_by_avg_review_data['category'] = new_bottom_avg_reviews_plot_data.Category.tolist()
        new_bottom_by_avg_review_data['average'] = new_bottom_avg_reviews_plot_data.average.tolist()
        new_bottom_by_avg_review_data['total'] = new_bottom_avg_reviews_plot_data.total.tolist()
        new_bottom_by_avg_review_data['color'] = new_colors

        p_bottom_k_by_total_reviews.x_range.factors = new_bottom_by_total_review_data['x_range']
        p_bottom_k_by_avg_reviews.x_range.factors = new_bottom_by_avg_review_data['x_range']

        ds_bottom_k_by_total_reviews.data = new_bottom_by_total_review_data
        ds_bottom_k_by_avg_reviews.data = new_bottom_by_avg_review_data

    def update_plot(attr, old, new):

        new_count = k_select_slider.value

        new_top_total_reviews_plot_data = top_category_by_total_reviews.head(new_count)
        new_bottom_total_reviews_plot_data = bottom_category_by_total_reviews.head(new_count)
        new_top_avg_reviews_plot_data = top_category_by_avg_reviews.head(new_count)
        new_bottom_avg_reviews_plot_data = bottom_category_by_avg_reviews.head(new_count)
        new_colors = getKColors(new_count)

        new_top_by_total_review_data = dict()
        new_top_by_total_review_data['x_range'] = new_top_total_reviews_plot_data.Category.tolist()
        new_top_by_total_review_data['category'] = new_top_total_reviews_plot_data.Category.tolist()
        new_top_by_total_review_data['average'] = new_top_total_reviews_plot_data.average.tolist()
        new_top_by_total_review_data['total'] = new_top_total_reviews_plot_data.total.tolist()
        new_top_by_total_review_data['color'] = new_colors

        new_bottom_by_total_review_data = dict()
        new_bottom_by_total_review_data['x_range'] = new_bottom_total_reviews_plot_data.Category.tolist()
        new_bottom_by_total_review_data['category'] = new_bottom_total_reviews_plot_data.Category.tolist()
        new_bottom_by_total_review_data['average'] = new_bottom_total_reviews_plot_data.average.tolist()
        new_bottom_by_total_review_data['total'] = new_bottom_total_reviews_plot_data.total.tolist()
        new_bottom_by_total_review_data['color'] = new_colors

        new_top_by_avg_review_data = dict()
        new_top_by_avg_review_data['x_range'] = new_top_avg_reviews_plot_data.Category.tolist()
        new_top_by_avg_review_data['category'] = new_top_avg_reviews_plot_data.Category.tolist()
        new_top_by_avg_review_data['average'] = new_top_avg_reviews_plot_data.average.tolist()
        new_top_by_avg_review_data['total'] = new_top_avg_reviews_plot_data.total.tolist()
        new_top_by_avg_review_data['color'] = new_colors

        new_bottom_by_avg_review_data = dict()
        new_bottom_by_avg_review_data['x_range'] = new_bottom_avg_reviews_plot_data.Category.tolist()
        new_bottom_by_avg_review_data['category'] = new_bottom_avg_reviews_plot_data.Category.tolist()
        new_bottom_by_avg_review_data['average'] = new_bottom_avg_reviews_plot_data.average.tolist()
        new_bottom_by_avg_review_data['total'] = new_bottom_avg_reviews_plot_data.total.tolist()
        new_bottom_by_avg_review_data['color'] = new_colors

        p_top_k_by_total_reviews.x_range.factors = new_top_by_total_review_data['x_range']
        p_bottom_k_by_total_reviews.x_range.factors = new_bottom_by_total_review_data['x_range']
        p_top_k_by_avg_reviews.x_range.factors = new_top_by_avg_review_data['x_range']
        p_bottom_k_by_avg_reviews.x_range.factors = new_bottom_by_avg_review_data['x_range']

        ds_top_k_by_total_reviews.data = new_top_by_total_review_data
        ds_bottom_k_by_total_reviews.data = new_bottom_by_total_review_data
        ds_top_k_by_avg_reviews.data = new_top_by_avg_review_data
        ds_bottom_k_by_avg_reviews.data = new_bottom_by_avg_review_data

    best_performing_button.on_click(update_best_performers)

    worst_performing_button.on_click(update_worst_performers)

    layout = column(heading_div,
                    row(column(row(best_performing_rating_text, best_performing_total_text),
                    best_performing_button),
                    column(row(worst_performing_rating_text, worst_performing_total_text),
                    worst_performing_button)),

                    row(p_top_k_by_total_reviews, p_bottom_k_by_total_reviews),

                    row(p_top_k_by_avg_reviews, p_bottom_k_by_avg_reviews))
    tab = Panel(child=layout, title='Parameterized - Category Wise Performance')
    return tab

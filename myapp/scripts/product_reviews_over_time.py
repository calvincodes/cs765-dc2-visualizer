from os.path import dirname, join

import pandas as pd
import numpy as np
import math

from bokeh.io import show, output_notebook, push_notebook
from bokeh.plotting import figure

from bokeh.models import CategoricalColorMapper, HoverTool, ColumnDataSource, Panel, NumeralTickFormatter
from bokeh.models.widgets import CheckboxGroup, Slider, RangeSlider, Tabs, RadioButtonGroup, Button, TextInput, Div, \
    PreText

from bokeh.layouts import column, row, WidgetBox
from bokeh.palettes import Category20_20

from bokeh.application.handlers import FunctionHandler
from bokeh.application import Application

from bokeh.plotting import figure, curdoc

from .helper import getKColors


def product_reviews_over_time_tab(dataset, metadata):
    combined_data = dataset.set_index('asin').join(metadata.set_index('Product ID')).reset_index()
    combined_data.columns = ['asin', 'reviewerID', 'overall', 'unixReviewTime', 'Description', 'price', 'Category']
    combined_data['asin'] = combined_data['asin'].astype(str)

    def get_product_data(product_id):
        product_data = combined_data[combined_data['asin'] == product_id]

        product_data['dtReviewTime'] = pd.to_datetime(product_data['unixReviewTime'], unit='s')
        product_data['reviewYear'] = product_data['dtReviewTime'].dt.strftime('%Y')
        product_data['reviewMonth'] = product_data['dtReviewTime'].dt.strftime('%Y-%m')
        product_data['dtReviewTime'] = product_data['dtReviewTime'].dt.strftime('%Y-%m-%d')
        product_data = product_data.sort_values('dtReviewTime')
        return product_data

    # Default selected_product is the most_purchased_product
    selected_product = combined_data.asin.value_counts().head(1).index[0]
    filtered_data = get_product_data(selected_product)

    top_k = 8 if len(combined_data) > 8 else len(combined_data)
    top_k_products = combined_data.asin.value_counts().head(top_k).keys().tolist()
    bottom_k_products = combined_data.asin.value_counts().sort_values(ascending=True).head(top_k).keys().tolist()

    product_details = dict()
    product_details['asin'] = filtered_data.head(1).asin.values[0]
    product_details['description'] = filtered_data.head(1).Description.values[0]
    product_details['category'] = filtered_data.head(1).Category.values[0]
    review_avg = filtered_data.groupby('Category')['overall'].agg(['mean', 'count']).reset_index()
    product_details['total_reviews'] = str(review_avg['count'].values[0])
    product_details['review_avg'] = str(review_avg['mean'].values[0])
    price_avg = filtered_data.groupby('Category')['price'].agg(['mean', 'count']).reset_index()
    product_details['price_avg'] = str(price_avg['mean'].values[0])

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
    r1_l = p1.line(source=source, x='time_stamp', y='total', line_width=2)
    r1_c = p1.circle(source=source, x='time_stamp', y='total', size=15, color="red", alpha=0.5)

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

    ds1_l = r1_l.data_source
    ds1_c = r1_c.data_source

    # Average Rating Figure
    p2 = figure(x_range=plot_data.time.tolist(), plot_width=1200, plot_height=300)
    r2_l = p2.line(source=source, x='time_stamp', y='average', line_width=2)
    r2_c = p2.circle(source=source, x='time_stamp', y='average', size=15, color="red", alpha=0.5)

    p2.add_tools(hover)

    # Formatting axes
    p2.xaxis.axis_label = "Time"
    p2.xaxis.major_label_orientation = math.pi / 2
    p2.xaxis.major_label_text_font_size = "10pt"
    p2.xaxis.axis_label_text_font_size = "15pt"

    p2.yaxis.axis_label = "Average Rating"
    p2.yaxis.formatter = NumeralTickFormatter(format="0")
    p2.yaxis.major_label_text_font_size = "10pt"
    p2.yaxis.axis_label_text_font_size = "15pt"

    ds2_l = r2_l.data_source
    ds2_c = r2_c.data_source

    radio_button_group = RadioButtonGroup(
        labels=["Yearly", "Monthly", "Daily"], active=0, width=1200)

    def get_updated_plot_data_dict(new_plot_data):

        new_data = dict()

        if new_plot_data.empty:
            new_data['x_range'] = []
            new_data['time_stamp'] = []
            new_data['average'] = []
            new_data['total'] = []
            new_data['color'] = []

        else:
            new_colors = getKColors(len(new_plot_data))

            new_data['x_range'] = new_plot_data.time.tolist()
            new_data['time_stamp'] = new_plot_data.time.tolist()
            new_data['average'] = new_plot_data.average.tolist()
            new_data['total'] = new_plot_data.total.tolist()
            new_data['color'] = new_colors

        return new_data

    def update_plot(attr, old, new):

        global year_wise_reviews, month_wise_reviews, date_wise_reviews, filtered_data, selected_product

        try:
            selected_product
        except NameError:
            selected_product = combined_data.asin.value_counts().head(1).index[0]

        filtered_data = get_product_data(selected_product)

        new_plot_data = plot_data

        if radio_button_group.active == 0:
            try:
                year_wise_reviews
            except NameError:
                year_wise_reviews = None

            year_wise_reviews = filtered_data.groupby('reviewYear')['overall'].agg(['mean', 'count']).reset_index()
            year_wise_reviews.columns = ['time', 'average', 'total']

            new_plot_data = year_wise_reviews

        if radio_button_group.active == 1:

            try:
                month_wise_reviews
            except NameError:
                month_wise_reviews = None

            month_wise_reviews = filtered_data.groupby('reviewMonth')['overall'].agg(
                ['mean', 'count']).reset_index()
            month_wise_reviews.columns = ['time', 'average', 'total']
            new_plot_data = month_wise_reviews

        if radio_button_group.active == 2:

            try:
                date_wise_reviews
            except NameError:
                date_wise_reviews = None

            date_wise_reviews = filtered_data.groupby('dtReviewTime')['overall'].agg(
                ['mean', 'count']).reset_index()
            date_wise_reviews.columns = ['time', 'average', 'total']
            new_plot_data = date_wise_reviews

        new_data = get_updated_plot_data_dict(new_plot_data)

        p1.x_range.factors = new_data['x_range']
        p2.x_range.factors = new_data['x_range']

        ds1_l.data = new_data
        ds1_c.data = new_data
        ds2_l.data = new_data
        ds2_c.data = new_data

    radio_button_group.on_change('active', update_plot)

    def generate_div_text(product_attributes):
        return """<table width="1200px" style='font-family: arial, sans-serif; border-collapse: collapse; width: 100%;'> 
                                        <tr> 
                                            <th style='border: 1px solid #dddddd; text-align: left; padding: 8px; align: center;'>Attribute</th> 
                                            <th style='border: 1px solid #dddddd; text-align: left; padding: 8px; align: center;'>Value</th> </tr>

                                        <tr> 
                                            <td style='border: 1px solid #dddddd; text-align: left; padding: 8px; align: center; background-color: #dddddd'>
                                                Product ID
                                            </td>
                                            <td style='border: 1px solid #dddddd; text-align: left; padding: 8px; align: center; background-color: #dddddd'>
                                                """ + product_attributes['asin'] + """
                                            </td>
                                        </tr>

                                        <tr> 
                                            <td style='border: 1px solid #dddddd; text-align: left; padding: 8px; align: center;'>
                                                Description
                                            </td>
                                            <td style='border: 1px solid #dddddd; text-align: left; padding: 8px; align: center'>
                                                """ + product_attributes['description'] + """
                                            </td>
                                        </tr>

                                        <tr> 
                                            <td style='border: 1px solid #dddddd; text-align: left; padding: 8px; align: center; background-color: #dddddd'>
                                                Category
                                            </td>
                                            <td style='border: 1px solid #dddddd; text-align: left; padding: 8px; align: center; background-color: #dddddd'>
                                                """ + product_attributes['category'] + """
                                            </td>
                                        </tr>

                                        <tr> 
                                            <td style='border: 1px solid #dddddd; text-align: left; padding: 8px; align: center;'>
                                                Total Reviews
                                            </td>
                                            <td style='border: 1px solid #dddddd; text-align: left; padding: 8px; align: center'>
                                                """ + str(product_attributes['total_reviews']) + """
                                            </td>
                                        </tr>

                                        <tr> 
                                            <td style='border: 1px solid #dddddd; text-align: left; padding: 8px; align: center; background-color: #dddddd'>
                                                Average Rating
                                            </td>
                                            <td style='border: 1px solid #dddddd; text-align: left; padding: 8px; align: center; background-color: #dddddd'>
                                                """ + str(product_attributes['review_avg']) + """
                                            </td>
                                        </tr>

                                        <tr> 
                                            <td style='border: 1px solid #dddddd; text-align: left; padding: 8px; align: center;'>
                                                Average Price
                                            </td>
                                            <td style='border: 1px solid #dddddd; text-align: left; padding: 8px; align: center'>
                                                """ + str(product_attributes['price_avg']) + """
                                            </td>
                                        </tr>

                                        </table>"""

    product_details_div = Div(text=generate_div_text(product_details), width=1200, height=300)

    def update_selection():

        global year_wise_reviews, month_wise_reviews, date_wise_reviews, product_details, filtered_data, selected_product
        selected_product = search_input.value
        searched_data = get_product_data(search_input.value)
        filtered_data = searched_data
        new_data = dict()

        if searched_data.empty:

            year_wise_reviews = searched_data
            month_wise_reviews = searched_data
            date_wise_reviews = searched_data

            new_data['x_range'] = []
            new_data['time_stamp'] = []
            new_data['average'] = []
            new_data['total'] = []
            new_data['color'] = []

            p1.x_range.factors = new_data['x_range']
            p2.x_range.factors = new_data['x_range']

            product_details_div.text = """<img alt="Sorry! No product found." src="/myapp/static/images/no_results_found.png">"""

        else:

            product_details = dict()

            product_details['asin'] = searched_data.head(1).asin.values[0]
            product_details['description'] = searched_data.head(1).Description.values[0]
            product_details['category'] = searched_data.head(1).Category.values[0]
            updated_review_avg = searched_data.groupby('Category')['overall'].agg(['mean', 'count']).reset_index()
            product_details['total_reviews'] = str(updated_review_avg['count'].values[0])
            product_details['review_avg'] = str(updated_review_avg['mean'].values[0])
            updated_price_avg = searched_data.groupby('Category')['price'].agg(['mean', 'count']).reset_index()
            product_details['price_avg'] = str(updated_price_avg['mean'].values[0])

            product_details_div.text = generate_div_text(product_details)

            year_wise_reviews = searched_data.groupby('reviewYear')['overall'].agg(['mean', 'count']).reset_index()
            year_wise_reviews.columns = ['time', 'average', 'total']

            month_wise_reviews = searched_data.groupby('reviewMonth')['overall'].agg(['mean', 'count']).reset_index()
            month_wise_reviews.columns = ['time', 'average', 'total']

            date_wise_reviews = searched_data.groupby('dtReviewTime')['overall'].agg(['mean', 'count']).reset_index()
            date_wise_reviews.columns = ['time', 'average', 'total']

            if radio_button_group.active == 0:
                new_plot_data = year_wise_reviews
            if radio_button_group.active == 1:
                new_plot_data = month_wise_reviews
            if radio_button_group.active == 2:
                new_plot_data = date_wise_reviews

            new_data = get_updated_plot_data_dict(new_plot_data)

            p1.x_range.factors = new_data['x_range']
            p2.x_range.factors = new_data['x_range']

        ds1_l.data = new_data
        ds1_c.data = new_data
        ds2_l.data = new_data
        ds2_c.data = new_data

    search_input = TextInput(value=selected_product, title="Product ID:")
    search_button = Button(label="Search", button_type="success")
    search_button.on_click(update_selection)

    top_k_pid_list = ""
    temp_count = 1
    for i in range(len(top_k_products)):
        # top_k_pid_list += top_k_products[i] + ", "
        if temp_count % 4 == 0:
            top_k_pid_list += top_k_products[i] + """<br>"""
            temp_count = 0
        else:
            top_k_pid_list += top_k_products[i] + ", "

        temp_count = temp_count + 1

    bottom_k_pid_list = ""
    temp_count = 1
    for i in range(len(bottom_k_products)):
        # bottom_k_pid_list += bottom_k_products[i] + ", "
        if temp_count % 4 == 0:
            bottom_k_pid_list += bottom_k_products[i] + """<br>"""
            temp_count = 0
        else:
            bottom_k_pid_list += bottom_k_products[i] + ", "

        temp_count = temp_count + 1

    pre_text_data = """<font size="4"><b>Here are a few sample product ids from your dataset:</b></font> <br><br>""" + \
                    """<font color="blue" size="3"><b>Top """ + str(top_k) + """ products:</b></font><br>""" + \
                    top_k_pid_list + """<br>""" + \
                    """<font color="red" size="3"><b>Bottom """ + str(top_k) + """ products:</b></font><br>""" + \
                    bottom_k_pid_list
    sample_product_ids = Div(text=pre_text_data, width=600, height=100)

    # layout = column(search_input, search_button, product_details_div, radio_button_group, p1, p2)
    layout = column(row(column(search_input, search_button, sample_product_ids), product_details_div),
                    radio_button_group, p1, p2)
    tab = Panel(child=layout, title='Product Reviews Timeline')
    return tab
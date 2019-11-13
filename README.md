# DESIGN CHALLENGE 2 | CS765 - Data Visualization

This application lets sellers visualize the customer review data of 
their products. Sellers can identify the best and worst performing 
categories, best and worst performing products in each category, and 
how are these products doing over time to find trends and patterns.

The application is hosted on Heroku: https://cs765-dc2-visualizer.herokuapp.com/myapp

Note: This uses an unpaid account and thus the load time of the 
application is approximately 30 seconds. Please don't give up as the
page loads.

TODO
1. Display msg upon successful load of data
2. Add some html to tell how to navigate
3. Search using text and provide results accordingly
5. Provide some sample analysis of data after upload. This may include mode of product, category, total products, etc. combined_data.asin.value_counts()
6. Mention in slider tab that it is static
7. Add link to sample data which can be downloaded and worked on.
8. Use default as worst performer in case of product review timeline.
9. Add more outlier. Top performing, worst performing. Most reviewers, least reviewers, etc.

`bokeh serve --show myapp/`

https://samirak93.github.io/analytics/Deploy-bokeh-server-plots-using-heroku.html

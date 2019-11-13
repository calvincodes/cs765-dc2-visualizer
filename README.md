# DESIGN CHALLENGE 2 | CS765 - Data Visualization

This application lets sellers visualize the customer review data of 
their products. Sellers can identify the best and worst performing 
categories, best and worst performing products in each category, and 
how are these products doing over time to find trends and patterns.

## Web Application

Hosted on Heroku: https://cs765-dc2-visualizer.herokuapp.com/myapp

Note: This uses an unpaid account and thus the load time of the 
application is **approximately 30 seconds**. Please don't give up as the
page loads.

## Local Setup

### Prerequisites

`pip install -r requirements.txt`

```
bokeh==1.4.0
Jinja2>=2.10.1
MarkupSafe==1.0
numpy==1.14.2
pandas==0.19.2
PyYAML>=4.2b1
requests==2.20.0
scikit-learn==0.19.1
scipy==1.0.1
tornado==5.0.1
```
### Running Locally

1. Clone the repository. `git clone https://github.com/calvincodes/cs765-dc2-visualizer.git`
2. Change directory to the cloned repository. `cd cs765-dc2-visualizer`
3. Install requirements if not already installed.
4. Run bokeh server. `bokeh serve --show myapp/`

## References
1. [Deploy Bokeh Server Plots Using Heroku](https://samirak93.github.io/analytics/Deploy-bokeh-server-plots-using-heroku.html)

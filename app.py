from flask import Flask, render_template

import plotly
import plotly.graph_objs as go
from plotly.offline import iplot
import plotly.express as px

import pandas as pd
import numpy as np
import json

# import and cleansing the data
data = pd.read_csv('hotel_booking.csv')
data.dropna(inplace=True)

# Change data types
data['arrival_date'] = data['arrival_date'].astype('datetime64')
data[['hotel', 'is_canceled']] = data[['hotel', 'is_canceled']].astype('category')  

# Feature Engineering
data['arrival_month'] = data['arrival_date'].dt.month_name()
no_canceled = data[data['is_canceled'] == 0]
month = ['January','February','March','April','May','June','July','August','September','November','December']

# Perform spatial analysis on guests home
def country_of_guests():
    country_guests = pd.crosstab(index=no_canceled['country'],columns='Number of guest').reset_index()

    plot_country_guests = px.choropleth(country_guests, 
                                        locations=country_guests['country'],
                                        color=country_guests['Number of guest'],
                                        hover_name=country_guests['country'],
                                        title=None)

    graphJSON = json.dumps(plot_country_guests, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

# Analysing the Most Busy Month
def busy_month():
    final_rush = pd.crosstab(index=no_canceled['arrival_month'], columns=no_canceled['hotel'])
    final_rush = final_rush.reindex(month)

    busy_month_plot = px.line(
        final_rush,
        x = final_rush.index,
        y = ['City Hotel', 'Resort Hotel'],
        title = None,
        labels = {
            'arrival_month':'Month',
            'variable':'Hotel',
            'value': 'Number of Booking'

        }

    )

    graphJSON = json.dumps(busy_month_plot, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


def create_line():
    N = 40
    x = np.linspace(0, 1, N)
    y = np.random.randn(N)
    df = pd.DataFrame({'x': x, 'y': y}) # creating a sample dataframe


    data2 = [
        go.Scatter(
            x=df['x'], # assign x as the dataframe column 'x'
            y=df['y']
        )
    ]

    graphJSON = json.dumps(data2, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


# This is code to create server using Flask
app = Flask(__name__)

# To connect with first page
@app.route('/')
def index():

    # Define your plot function here
    country_of_guests_plot = country_of_guests()
    busy_month_plot = busy_month()
    
    # Render your plot to first (index.html) page
    return render_template(
        'index.html',
        country_of_guests_plot=country_of_guests_plot,
        busy_month_plot=busy_month_plot

    )

# To connect with second page
@app.route('/analysis')
def analysis():

    # Define your plot function here
    line = create_line()

    # Render your plot to second (analysis.html) page
    return render_template(
        'analysis.html',
        lineplot=line
    )

if __name__ == '__main__':
    app.run()
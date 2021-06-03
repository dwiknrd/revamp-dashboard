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

    busy_month_plot = px.line(final_rush,
                              x = final_rush.index,
                              y = ['City Hotel', 'Resort Hotel'],
                              labels = {'arrival_month': 'Month',
                                        'variable': 'Hotel',
                                        'value': 'Number of Booking'})

    graphJSON = json.dumps(busy_month_plot.update_traces(mode='markers+lines'), cls=plotly.utils.PlotlyJSONEncoder)

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

# Month with the Highest Average Daily Rate
def month_highestADR():
    adr_month_hotel =  data.groupby(['arrival_month', 'hotel']).mean()['adr'].round(2).reset_index()
    adr_month_hotel['arrival_month'] = pd.Categorical(adr_month_hotel['arrival_month'], categories = month)
    adr_month_hotel = adr_month_hotel.sort_values('arrival_month')

    highestADR_plot = px.bar(adr_month_hotel, 
                             x = 'arrival_month', 
                             y = 'adr', 
                             color = 'hotel', 
                             barmode = 'group',
                             labels = {'arrival_month': 'Month', 
                                       'hotel' : 'Hotel',
                                       'adr': 'Average Daily Rate'})

    graphJSON = json.dumps(highestADR_plot, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

# Guests Distirbution for each Hotel
def guests_dist():
    check_out_hotel = no_canceled.groupby('hotel').sum()[['adults', 'children']].reset_index()
    check_out_hotel['total_guests'] = check_out_hotel['adults'] + check_out_hotel['children']

    for i in check_out_hotel.columns[1:4]:
        check_out_hotel[i] = (check_out_hotel[i] / check_out_hotel['total_guests'] * 100).round(2)
    
    check_out_hotel =  check_out_hotel.melt(id_vars = 'hotel', value_vars = ['adults', 'children'])

    guests_dist_plot = px.bar(check_out_hotel,
                              x = 'value',
                              y = 'variable',
                              color = 'hotel',
                              barmode='group',
                              labels = {'value': 'Percentage Guests',
                              'variable': 'Age Group',
                              'hotel': 'Hotel'})

    graphJSON = json.dumps(guests_dist_plot, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

# Highest Cancellation Rate
def cancel_rate():
    cancel = data[data['is_canceled'] == 1]
    cancel['arrival_month'] = cancel['arrival_date'].dt.month_name()
    
    cancel_agg = pd.crosstab(index = cancel['arrival_month'],
             columns = cancel['hotel'])
    
    cancel_agg = cancel_agg.reindex(month)

    cancel_rate_plot = px.line(cancel_agg, 
                               x = cancel_agg.index,
                               y = ['City Hotel', 'Resort Hotel'],
                               title = 'Highest Cancellation Rate',
                               labels = {'arrival_month': 'Month',
                               'variable': 'Hotel',
                               'value': 'Number of Canceled Orders'})

    graphJSON = json.dumps(cancel_rate_plot.update_traces(mode='markers+lines'), cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


# This is code to create server using Flask
app = Flask(__name__)

# To connect with first page
@app.route('/')
def index():

    # Define your plot function here
    country_of_guests_plot = country_of_guests()
    
    
    # Render your plot to first (index.html) page
    return render_template(
        'index.html',
        country_of_guests_plot=country_of_guests_plot

    )

# To connect with second page
@app.route('/analysis')
def analysis():

    # Define your plot function here
    busy_month_plot = busy_month()

    # Render your plot to second (analysis.html) page
    return render_template(
        'analysis.html',
        busy_month_plot=busy_month_plot
    )

    # Define your plot function here
    highestADR_plot = month_highestADR()

    # Render your plot to second (analysis.html) page
    return render_template(
        'analysis.html',
        highestADR_plot=highestADR_plot
    )

    # Define your plot function here
    guests_dist_plot = guests_dist()

    # Render your plot to second (analysis.html) page
    return render_template(
        'analysis.html',
        guests_dist_plot=guests_dist_plot
    )

    # Define your plot function here
    cancel_rate_plot = cancel_rate()

    # Render your plot to second (analysis.html) page
    return render_template(
        'analysis.html',
        cancel_rate_plot=cancel_rate_plot
    )

    # Define your plot function here
    lineplot = create_line()

    # Render your plot to second (analysis.html) page
    return render_template(
        'analysis.html',
        lineplot=lineplot
    )
    
    

if __name__ == '__main__':
    app.run()
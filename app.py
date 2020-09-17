from flask import Flask, render_template, request, redirect
import pandas as pd
import numpy as np
import bokeh
import requests
from bokeh.layouts import gridplot
from bokeh.plotting import figure, output_file, save

app = Flask(__name__)
app.vars={}

def datetime(x):
    return np.array(x, dtype=np.datetime64)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('stock_ticker.html')
    else:
        if request.form['ticker'] == '':
            ticker = 'TSLA'
        else:
            ticker = request.form['ticker']
        app.vars['ticker'] = ticker
        app.vars['features'] = request.form.getlist('features')
        features = app.vars['features']
       
        url="https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol="+ticker+"&apikey=Z8PIBV7276PKM1RY"
        response = requests.get(url)
        data = response.json()
        data1 = data["Time Series (Daily)"]
        df = pd.DataFrame(data1).transpose()
        df.columns = ['open', 'high', 'low', 'close', 'adj_close', 'volume', 'dividend amount', 'split coefficient']
        df1 = df[features]

#        plot stack graph
        p = figure(x_axis_type="datetime", title=ticker+" price history", y_range=(df1.min()[0], df1.max()[0]))
        p.grid.grid_line_alpha = 0
        p.xaxis.axis_label = 'Date'
        p.yaxis.axis_label = 'Price'
        p.ygrid.band_fill_color = "olive"
        p.ygrid.band_fill_alpha = 0.1
        
        if 'open' in features:
            p.line(datetime(df1.index), df1['open'], legend_label='open', color='pink')
        if 'close' in features:
            p.line(datetime(df1.index), df1['close'], legend_label='close', color='green')
        if 'adj_close' in features:
            p.line(datetime(df1.index), df1['adj_close'], legend_label='adjusted close', color='blue')
        if 'high' in features:
            p.circle(datetime(df1.index), df1['high'], size=8, legend_label='high',
          color='red', alpha=0.4)
        if 'low' in features:
            p.triangle(datetime(df1.index), df1['low'], size=8, legend_label='low',
          color='orange', alpha=0.4)
        p.legend.location="top_left"
        output_file("templates/stocks_history.html", title="stocks price history")
        save(p)

        return render_template('stocks_history.html')




@app.route('/about')
def about():
  return render_template('about.html')

if __name__ == '__main__':
  app.run(debug=True)

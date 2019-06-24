import pandas as pd
from flask import Flask, render_template, request
#from bokeh.embed import components
from bokeh.models import HoverTool
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html
from alpha_vantage.timeseries import TimeSeries
#from jinja2 import Template

#Connect the app
app = Flask(__name__)

#Helper function
def get_plot(data):
    #Make plot and customize
    p = figure()
    numrows = len(data)
    minutes = list(range(0,numrows))
    p.line(x=minutes, y=data['4. close'])
    p.title.text_font_size = '16pt'
    p.add_tools(HoverTool()) #Need to configure tooltips for a good HoverTool

    #Return the plot
    return(p)

@app.route('/')
def homepage():
    return render_template('home.html')

@app.route('/result', methods = ['POST'])
def result():
    if request.method == "POST":
            tickersymbol = request.form['tickersymbol']

    #Get stock data from alpha vantage
    ts = TimeSeries(key='16KLHH243AJ34AEX', output_format='pandas')
    data, meta_data = ts.get_intraday(symbol=tickersymbol,interval='1min', outputsize='full')

    #Generate plot and render html
    myplot = get_plot(data)
    html = file_html(myplot, CDN, "my plot")

    return render_template('result.html', tickersymbol=tickersymbol, html=html)

if __name__ == '__main__':
    app.run(debug=True) #Set to false when deploying

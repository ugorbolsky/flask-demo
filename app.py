from flask import Flask, render_template, request, redirect
import json
import urllib2
import pandas as pd
from bokeh.charts import TimeSeries
from bokeh.embed import components
from bokeh.plotting import figure

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def main():
  return redirect('/index')


@app.route('/index', methods=['GET'])
def index():
  return render_template('index.html')


@app.route('/index', methods=['POST'])
def index2():
	app.ticker=request.form['ticker']
	return redirect('/plot_app')


@app.route('/plot_app', methods=['GET','POST'])
def plot_app():
        tic='GOOG'
	url='https://www.quandl.com/api/v3/datasets/WIKI/'+tic+'.json?api_key=a5_n4JFYrNmGQcPUrG7d'
	json_obj= urllib2.urlopen(url)
	data = json.load(json_obj)

	last_month=data['dataset']['data'][0:30]
	date=[]
	quotes=[]
	for i in last_month:
    		date.insert(0,str(i[0]))
    		quotes.insert(0,i[4])
	plot = figure(title='Data from Quandle WIKI set',y_axis_label='quote, $',x_axis_label='date', x_axis_type='datetime')
	plot.line(date, quotes)

	#plotting_data=pd.DataFrame({'Quote':quotes}, index=date)
	#plot = TimeSeries(plotting_data, title="Stock prices, previous 30 days", ylabel='Stock Price', xlabel='Date')
	app_script, app_div = components(plot)
	app_head='<link rel="stylesheet" href="https://cdn.pydata.org/bokeh/release/bokeh-0.11.1.min.css" type="text/css" />\
<script type="text/javascript" src="https://cdn.pydata.org/bokeh/release/bokeh-0.11.1.min.js"></script>\
<script type="text/javascript"> Bokeh.set_log_level("info");</script>'

	return render_template('plot.html', head =app_head, ticker=tic, script=app_script, div=app_div)

if __name__ == '__main__':
  app.run(port=33507)

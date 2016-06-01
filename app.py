from flask import Flask, render_template, request, redirect
import urllib2
import json
import pandas as pd
from bokeh.charts import TimeSeries
from bokeh.embed import components



app = Flask(__name__)

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
	ticker=app.ticker
	url='https://www.quandl.com/api/v3/datasets/WIKI/'+ticker+'.json'
	json_obj= urllib2.urlopen(url)
	data = json.load(json_obj)

	last_month=data['dataset']['data'][0:30]
	date=[]
	quotes=[]
	for i in last_month:
    		date.append(i[0])
    		quotes.append(i[4])

	plotting_data=pd.DataFrame({'Quote':quotes}, index=date)
	plot = TimeSeries(plotting_data, title="Stock prices, previous 30 days", ylabel='Stock Price', xlabel='Date')
	script, div = components(plot)
	return render_template('plot.html', ticker=app.ticker,script=script, div=div)


if __name__ == '__main__':
  app.run(port=33507)

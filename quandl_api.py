import urllib2
import json
import pandas as pd
from bokeh.charts import TimeSeries, output_file, show
from bokeh.embed import components


ticker='GOOG'
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
output_file("timeseries.html")
p = TimeSeries(plotting_data, title="Stock prices, last 30 days", ylabel='Stock Price', xlabel='Date')
show(p)


import datetime as dt
from gsvi.connection import GoogleConnection
from gsvi.timeseries import SVSeries
import pandas as pd

start_year = 2004
end_year = 2019
start_month = 1
end_month = 12
start_day = 1
end_day = 30
search_word = 'Fintech'
region = input('Please input region: ')


start = dt.datetime(year=start_year, month=start_month, day=start_day)
end = dt.datetime(year=end_year, month=end_month, day=end_day)

connection = GoogleConnection()
series = SVSeries.univariate(
    connection=connection,
    query={'key': search_word, 'geo': region},
    start=start, end=end, granularity='MONTH'
)

google_data = series.get_data()

df = pd.DataFrame(google_data)
#df.rename(columns= 'Date')
print(df)
Cs = df.to_csv('iran_trends.csv')
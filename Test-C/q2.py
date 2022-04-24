import requests
import pandas as pd

def get_data():


    url = 'https://data.kingcounty.gov/api/views/f29f-zza5/rows.csv?accessType=DOWNLOAD'
    r = requests.get(url, allow_redirects=True)
    open('q2.csv', 'wb').write(r.content)

def load_data():
    df = pd.read_csv('q2.csv')
    print(df.head())
    return df



df = load_data()

def aggregare(df):
    df['Date'] = pd.to_datetime(df['Inspection Date'])
    df = df.groupby(['Date', pd.Grouper(key='Date', freq='W')]).count().reset_index()
    #.sort_values('Date')
    return df

def aggregare2(df):
    df['Date'] = pd.to_datetime(df['Inspection Date'])
    df['weekday'] = df['Date'].dt.dayofweek
    qty =  df.resample('W', on='Date').agg({'Inspection_Serial_Num':'unique'}).reset_index()
    qty['qty'] = qty.apply(lambda x:len(x['Inspection_Serial_Num']), axis =1)
    score = df.resample('W', on='Date').agg({'Violation Points':'mean'}).reset_index()
    day_score = df.groupby(['weekday']).mean()
    return day_score,qty,score
day_score, qty,score = aggregare2(df)
print(qty)
print(score)
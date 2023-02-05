import requests


def get_data_from_YFinance_API():
    #replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=1min&apikey=demo'
    r = requests.get(url)
    data = r.json()
    print(data)
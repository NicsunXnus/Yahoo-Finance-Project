import yfinance as yf
#import html5lib
import yahoo_fin.stock_info as si
from futu import *
import pandas as pd

#Ticker = yf.Ticker("D05.SI")
#print(Ticker.info)
###print(Ticker.info["trailingPE"])
##period_data = Ticker.history(period= '10d')['Volume']
##print(period_data)
###For day0 to day-4
##print(period_data[5:10])
###For day-5 to day-9
##print(period_data[0:5])
      

##for key,val in Ticker.info.items():
##    print(key)
##print("\n-----------------Financials----------------------")
##print(Ticker.financials)
##print("\n-----------------Quarter_Financials------------------------")
##print(Ticker.quarterly_financials)
##print("\n-------------Balance_Sheet----------------------")
##print(Ticker.balance_sheet)
##print("\n------------Quarter_balance_sheet-----------------")
##print(Ticker.quarterly_balance_sheet)
##print("\n-----------cashflow----------------------------")
##print(Ticker.cashflow)
##print("\n------------earnings--------------------------")
##print(Ticker.earnings)
##print("\n----------sustainability---------------------")
##print(Ticker.sustainability)
##print("\n--------recommendations-----------------------")
##print(Ticker.recommendations)
##print("\n-----earnings_dates---------------")
##print(Ticker.earnings_dates)
##print("\n----isin---------")
##print(Ticker.isin)
##print("\n---options------------------")
##print(Ticker.options)
##print("\n---Analysis------------------")
##print(Ticker.analysis)
##
##for x in range(20):
##    stats=si.get_quote_data("AAPL")
##    #print(stats)
##quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
##simple_filter = SimpleFilter()
##simple_filter.filter_min = 2
##simple_filter.filter_max = 1000
##simple_filter.stock_field = StockField.CUR_PRICE
##simple_filter.is_no_filter = False
##test = quote_ctx.get_stock_filter(market=Market.US, filter_list=[simple_filter],begin=0)
##print(quote_ctx.query_subscription(True))


##from urllib.request import urlopen
##import json
##import time
##
##class GoogleFinanceAPI:
##    def __init__(self):
##        self.prefix = "http://finance.google.com/finance/info?client=ig&q="
##    
##    def get(self,symbol,exchange):
##        url = self.prefix+"%s:%s"%(exchange,symbol)
##        u = urlopen(url)
##        content = u.read()
##        
##        obj = json.loads(content[3:])
##        return obj[0]
##        
##        
##c = GoogleFinanceAPI()
##quote = c.get("MSFT","NASDAQ")

import os
import requests

base_url = 'https://cloud.iexapis.com/stable/'
sandbox_url = 'https://sandbox.iexapis.com/stable'

token = os.environ.get('IEX_TOKEN')
params = {'token': token}

#resp = requests.get(base_url + '/status')
##resp = requests.get(base_url+'stock/AAPL/chart', params=params)
##try:
##    resp.raise_for_status()
##except Exception as error:
##    print("Error:" + str(error))
#print(resp.json())

##df = pd.DataFrame(resp.json())
##
##print(df.head())

def historical_data(_symbol, _range=None, _date=None):
    endpoint = f'{base_url}/stock/{_symbol}/chart'
    if _range:
        endpoint += f'/{_range}'
    elif _date:
        endpoint += f'/date/{_date}'
    
    resp = requests.get(endpoint, params=params)
    resp.raise_for_status()
    return pd.DataFrame(resp.json())

#appl_3m_df = historical_data('AAPL', _range='3m')
#appl_april_20_df = historical_data('AAPL', _date=20200420)
#print(appl_3m_df.head())

##earnings
#endpoint = '/stock/market/today-earnings'
##news
#endpoint = '/stock/TSLA/news'
#resp = requests.get(base_url+endpoint, params=params)

##payload = params.copy()
##payload['symbols'] = 'TSLA, NFLX'
##resp = requests.get(base_url+'/tops/last', params=payload)
##resp=requests.get(base_url+'/ref-data/exchanges', params=params)
##df = pd.DataFrame(resp.json())
##df.to_csv(r'C:\Users\nicky\OneDrive\Desktop\IX.csv')
##resp=requests.get(base_url+'/stable/rules/schema', params=params)
##print(resp)
##df = pd.DataFrame(resp.json())
##print(df)
#df.to_csv(r'C:\Users\nicky\OneDrive\Desktop\Rules.csv')

##from iexfinance.refdata import get_symbols
##from iexfinance.refdata import get_iex_symbols
##from iexfinance.refdata import get_exchange_symbols
###print(type(get_symbols()))
##get_exchange_symbols("XDUB").to_csv(r'C:\Users\nicky\OneDrive\Desktop\IrelandSymbols.csv')
##

import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
# US english
LANGUAGE = "en-US,en;q=0.5"

def get_soup(url):
    """Constructs and returns a soup using the HTML content of `url` passed"""
    # initialize a session
    session = requests.Session()
    # set the User-Agent as a regular browser
    session.headers['User-Agent'] = USER_AGENT
    # request for english content (optional)
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    # make the request
    html = session.get(url)
    # return the soup
    return bs(html.content, "html.parser")
def get_all_tables(soup):
    """Extracts and returns all tables in a soup object"""
    return soup.find_all("table")
def get_table_headers(table):
    """Given a table soup, returns all the headers"""
    headers = []
    for th in table.find("tr").find_all("th"):
        headers.append(th.text.strip())
    return headers
def get_table_rows(table):
    """Given a table, returns all its rows"""
    rows = []
    for tr in table.find_all("tr")[1:]:
        cells = []
        # grab all td tags in this table row
        tds = tr.find_all("td")
        if len(tds) == 0:
            # if no td tags, search for th tags
            # can be found especially in wikipedia tables below the table
            ths = tr.find_all("th")
            for th in ths:
                cells.append(th.text.strip())
        else:
            # use regular td tags
            for td in tds:
                cells.append(td.text.strip())
        rows.append(cells)
    return rows
def save_as_csv(table_name, headers, rows):
    df = pd.DataFrame(rows, columns=headers)
    print(df.size)
    df.to_csv(f"{table_name}.csv")
##
##   
##    
def main(url):
    # get the soup
    soup = get_soup(url)
    # extract all the tables from the web page
    tables = get_all_tables(soup)
    print(f"[+] Found a total of {len(tables)} tables.")
    # iterate over all tables
    for i, table in enumerate(tables, start=1):
        # get the table headers
        headers = get_table_headers(table)
        # get all the rows of the table
        rows = get_table_rows(table)
        # save table as csv file
        table_name = f"table-{i}"
        print(f"[+] Saving {table_name}")
        save_as_csv(table_name, headers, rows)
##
##def save_as_excel(headers,rows,writer):
##    df = pd.DataFrame(rows, columns=headers)
##    df.to_excel(writer,"Sheet 1") 

def get_table(url):
    # get the soup
    soup = get_soup(url.format(offset = 0))
    # extract all the tables from the web page
    table = get_all_tables(soup)[0]
    #print(f"[+] Found it.")
    # get the table headers
    headers = get_table_headers(table)
    # get all the rows of the table
    rows = get_table_rows(table)

    count = 2
    offset_value = 100
    startrow = 101
    newFile=r'C:\Users\nicky\OneDrive\Desktop\stocklist.xlsx'
    writer = pd.ExcelWriter(newFile, engine="xlsxwriter")
    #First 100 data
    df = pd.DataFrame(rows, columns=headers)
    df.to_excel(writer, "Sheet 1")
    while (df.size > 0):
        soup = get_soup(url.format(offset = offset_value))
        tables = get_all_tables(soup)
        try:
            table = tables[0]
        except Exception as error:
            print(error)
            break
        rows = get_table_rows(table)
        df = pd.DataFrame(rows)
        if (df.size == 0):
            break
        df.to_excel(writer, sheet_name = "Sheet 1", startrow=startrow, header=False)
        print("offset: ", offset_value)
        offset_value += 100
        startrow += 100
        print("count: ",count, "\n")
        count += 1
    writer.save()        

def get_market_data(market):
    #1. SG, 2. US, 3. CH, 4. HK, 5. JP, 6. Crypto
    yahoo_url = ["https://finance.yahoo.com/screener/unsaved/2052a280-261d-461a-8d7c-63ecc7e58f68?offset={offset:d}&count=100",
                 "https://finance.yahoo.com/screener/unsaved/c1f84a96-1001-4b1b-8ef3-401378cf9553?offset={offset:d}&count=100",
                 "https://finance.yahoo.com/screener/unsaved/961b8bcd-2a93-4111-8bea-c170b94af7fd?offset={offset:d}&count=100",
                 "https://finance.yahoo.com/screener/unsaved/0b45becc-1d90-4b52-8c83-7db3fc70b3f0?offset={offset:d}&count=100",
                 "https://finance.yahoo.com/screener/unsaved/f6fc792f-5015-4dc7-807f-2ae63103e7e7?offset={offset:d}&count=100",
                 "https://finance.yahoo.com/cryptocurrencies/?offset={offset:d}&count=100"]
    if (market == "SG"):
        get_table(yahoo_url[0])
    if (market == "US"):
        get_table(yahoo_url[1])
    if (market == "CH"):
        get_table(yahoo_url[2])
    if (market == "HK"):
        get_table(yahoo_url[3])
    if (market == "JP"):
        get_table(yahoo_url[4])
    if (market == "CR"):
        get_table(yahoo_url[5])

##value = 100
txt = "https://finance.yahoo.com/screener/unsaved/2052a280-261d-461a-8d7c-63ecc7e58f68?offset={offset:d}&count=100"
##print(txt.format(offset = value))

#main('https://finance.yahoo.com/screener/ce90da8a-e121-4510-bb64-917f8cb08463?offset=0&count=100')
#main('https://finance.yahoo.com/screener/unsaved/2052a280-261d-461a-8d7c-63ecc7e58f68?dependentField=sector&dependentValues=&offset=0&count=100')
#main('https://finance.yahoo.com/screener/unsaved/2052a280-261d-461a-8d7c-63ecc7e58f68?count=100&dependentField=sector&dependentValues=&offset=600')
##      https://finance.yahoo.com/screener/unsaved/2052a280-261d-461a-8d7c-63ecc7e58f68?count=100&dependentField=sector&dependentValues=&offset=100
##      https://finance.yahoo.com/screener/unsaved/2052a280-261d-461a-8d7c-63ecc7e58f68?count=100&dependentField=sector&dependentValues=&offset=200
##      https://finance.yahoo.com/screener/unsaved/2052a280-261d-461a-8d7c-63ecc7e58f68?count=100&dependentField=sector&dependentValues=&offset=300
##      https://finance.yahoo.com/screener/unsaved/2052a280-261d-461a-8d7c-63ecc7e58f68?count=100&dependentField=sector&dependentValues=&offset=400
##      https://finance.yahoo.com/screener/unsaved/2052a280-261d-461a-8d7c-63ecc7e58f68?count=100&dependentField=sector&dependentValues=&offset=500
get_market_data("JP")
#main("https://finance.yahoo.com/cryptocurrencies/?offset=300&count=100")

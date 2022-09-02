from bs4 import BeautifulSoup as bs
import datetime
import pandas as pd
import requests
import yfinance as yf

#YOU CAN IGNORE THEM
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
# US english
LANGUAGE = "en-US,en;q=0.5"

##HELPER METHODS: YOU CAN IGNORE THEM
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

#READ INSIDE THIS METHOD
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
    #HERE YOU MUST CHANGE THE PATH TO SUIT YOUR OWN COMPUTER
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
    print("---Finished extracting stock symbols from this market---\n")
    writer.save()        

# market = "SG"/"US"/"CH"/"HK"/"JP"/"CR"
# What this method does: Downloads the stock information from the specified
# region into an excel sheet.
# Information contains:
# Symbol /Name /Price (Intraday)/Change/% Change/Volume/Avg Vol (3 month)/Market Cap/PE Ratio (TTM)
# This method is mainly used to just collect the stock symbols as the larger collection of information
# is obtained from the yfinance.Ticker("Some ticker").info command
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


#initialise stocklist
#get_market_data("SG") #default is Singapore market,change it if you want to do so
                      # This will always create the stocklist excel file.
                      # You can comment this part out if you already have the stocklist
                      # file. Just add a hashtag in front of the line.

##Note, will take quite a while: Approximate 10 items for 2 minutes 6 s

#Read stocklist file
tickers = pd.read_excel(r'C:\Users\nicky\OneDrive\Desktop\stocklist.xlsx')
#Initialise yfinance
yf.pdr_override()
startrow = 1
#This part for creating the initial file
newFile = r'C:\Users\nicky\OneDrive\Desktop\Output1.xlsx'
writer = pd.ExcelWriter(newFile, engine="xlsxwriter")
headers = pd.DataFrame(columns=["symbol", "company name", "last price/price intraday", "change", "change %", "day low", "day high", "52 weeks low", "52 weeks high", "50 days moving average of share price",
           "200 days moving average of share price", "target low price", "target median price", "target mean price", "target high price", "volume",
           "average daily volume (10days)", "average volume (3 months)", "market capitalisation", "enterprise value", "trailing price to earning (PE)", "forward PE", "PEG ratio",
           "price to book value", "price to revenue", "EBITDA", "earning per share (EPS) (TTM or trailing)", "EPS est. next year or forward EPS",
           "dividend yield", "trailing annual dividend yield", "forward annual dividend yield",  "ex-dividend date", "current year revenue",
           "previous year revenue", "revenue growth (yearly)", "revenue per share", "current year net income (applicable to common shares)",
           "previous year net income",
           "current quarter revenue", "previous quarter revenue", "revenue growth (quarter)", "current quarter net income (applicable to common shares)",
           "previous quarter net income", "cash", "debt (short term + long term)", "book value", "intangible assets", "goodwill",
           "cash per share", "gross margin", "EBITDA margin", "profit margin",  "% held by insiders (heldPercentInsiders)",
           "% held by Instititutions (heldPercentInstitutions)", "% of short vs float (shortpercentoffloat)", "exchange", "industry", "sector",
           "financial currency"])

headers.to_excel(writer,sheet_name = "Sheet 1",startcol=0,index=False)
#Required items:
items_dict_to_be_copied = {'symbol': None,'name': None, 'last price':None,'change':None,'change %':None,'dayLow': None,'dayHigh':None,'fiftyTwoWeekLow':None, 'fiftyTwoWeekHigh':None,'fiftyDayAverage':None,
                           'twoHundredDayAverage':None,'targetLowPrice':None,'targetMedianPrice':None,'targetMeanPrice':None,'targetHighPrice':None,'volume':None,
                           'averageDailyVolume10Day':None,'averageVolume3months':None,'marketCap':None,'enterpriseValue':None,
                           'trailingPE':None, 'forwardPE':None,'pegRatio':None,'priceToBook':None,'priceToRevenue':None,'ebitda':None,'trailingEps':None,'forwardEps':None,
                           'dividendYield':None,'trailingAnnualDividendYield':None,'forwardAnnualDividendYield':None,'exDividendDate':None,
                           'current year revenue':None,'previous year revenue':None,'revenueGrowth':None,'revenuePerShare':None,
                           'current year net income (applicable to common shares)':None,'previous year net income':None,
                           'current quarter revenue':None,'previous quarter revenue':None,'revenueQuarterlyGrowth':None,
                           'current quarter net income (applicable to common shares)':None,'previous quarter net income':None,
                           'totalCash':None,'totalDebt':None,'bookValue':None,'Intangible Assets':None,
                           'Good Will':None, 'totalCashPerShare':None,'grossMargins':None,
                           'ebitdaMargins':None,'profitMargins':None,'heldPercentInsiders':None,'heldPercentInstitutions':None,'shortPercentOfFloat':None,'exchange':None,
                           'industry':None,'sector':None, 'currency':None}
for i in tickers.index[:4]:
    required_items = items_dict_to_be_copied.copy()
    stock = str(tickers["Symbol"][i])
    name = str(tickers["Name"][i])
    print(i, " ",stock, " ",name)
    required_items['symbol'] = stock
    required_items['name'] = name
    required_items['last price'] = str(tickers["Price (Intraday)"][i])
    required_items['change'] = str(tickers["Change"][i])
    required_items['change %'] = str(tickers["% Change"][i])
    required_items['averageVolume3months'] = str(tickers["Avg Vol (3 month)"][i])
    ticker = yf.Ticker(stock)
    try:
        #This part is for info
        info_dict = ticker.info
        for key,value in info_dict.items():
            try:
                if (key in required_items):
                    if (key == 'exDividendDate'):
                        print()
                        date = datetime.datetime.fromtimestamp(value)
                        required_items[key] = str(date)
                        continue
                    required_items[key] = value
            except Exception:
                print("Error with ",key," ",value)
        #This part for financials
        financials_df = ticker.financials.T
        if ('Total Revenue' in financials_df.columns):
            try:
                revenue_data = financials_df.loc[:,'Total Revenue']
                curr_yr_revenue = revenue_data[0]
                required_items['current year revenue'] = curr_yr_revenue
                prev_yr_revenue = revenue_data[1]
                required_items['previous year revenue'] = prev_yr_revenue
            except Exception:
                print("Not enough yearly revenue data")
        if ('Net Income Applicable To Common Shares' in financials_df.columns):
            try:
                income_data = financials_df.loc[:,'Net Income Applicable To Common Shares']
                curr_yr_income = income_data[0]
                required_items['current year net income (applicable to common shares)'] = curr_yr_income
                prev_yr_income = income_data[1]
                required_items['previous year net income'] = prev_yr_income
            except Exception:
                print("Not enough yearly income data")
##        if ('Ebit' in financials_df.columns):
##            try:
##                ebit_data = financials_df.loc[:,'Ebit']
##                curr_yr_ebit = ebit_data[0]
##                required_items['current year EBIT'] = curr_yr_ebit
##                prev_yr_ebit = ebit_data[1]
##                required_items['previous year EBIT'] = prev_yr_ebit
##            except Exception:
##                print("Not enough yearly ebit data")
##        if ('Extraordinary Items' in financials_df.columns):
##            try:
##                extra_items_data = financials_df.loc[:,'Extraordinary Items']
##                curr_yr_extra_items = extra_items_data[0]
##                required_items['current year extraordinary items'] = curr_yr_extra_items
##                prev_yr_extra_items = extra_items_data[1]
##                required_items['previous year extraordinary items'] = prev_yr_extra_items
##            except Exception:
##                print("Not enough yearly extraordinary items data")

        #This part for quarter financials
        quarterly_financials_df = ticker.quarterly_financials.T
        if ('Total Revenue' in quarterly_financials_df.columns):
            try:
                revenue_data = quarterly_financials_df.loc[:,'Total Revenue']
                curr_yr_revenue = revenue_data[0]
                required_items['current quarter revenue'] = curr_yr_revenue
                prev_yr_revenue = revenue_data[1]
                required_items['previous quarter revenue'] = prev_yr_revenue
            except Exception:
                print("Not enough quarterly revenue data")
        if ('Net Income Applicable To Common Shares' in quarterly_financials_df.columns):
            try:
                income_data = quarterly_financials_df.loc[:,'Net Income Applicable To Common Shares']
                curr_yr_income = income_data[0]
                required_items['current quarter net income (applicable to common shares)'] = curr_yr_income
                prev_yr_income = income_data[1]
                required_items['previous quarter net income'] = prev_yr_income
            except Exception:
                print("Not enough quarterly income data")
##        if ('Ebit' in quarterly_financials_df.columns):
##            try:
##                ebit_data = quarterly_financials_df.loc[:,'Ebit']
##                curr_yr_ebit = ebit_data[0]
##                required_items['current quarter EBIT'] = curr_yr_ebit
##                prev_yr_ebit = ebit_data[1]
##                required_items['previous quarter EBIT'] = prev_yr_ebit
##            except Exception:
##                print("Not enough quarterly ebit data")
##        if ('Extraordinary Items' in quarterly_financials_df.columns):
##            try:
##                extra_items_data = quarterly_financials_df.loc[:,'Extraordinary Items']
##                curr_yr_extra_items = extra_items_data[0]
##                required_items['current quarter extraordinary items'] = curr_yr_extra_items
##                prev_yr_extra_items = extra_items_data[1]
##                required_items['previous quarter extraordinary items'] = prev_yr_extra_items
##            except Exception:
##                print("Not enough quarterly extraordinary items data")
        #For balance sheet
        balance_sheet_df = ticker.balance_sheet.T
        if ('Good Will' in balance_sheet_df.columns):
            try:
                good_will_data = balance_sheet_df.loc[:,'Good Will']
                curr_yr_good_will = good_will_data[0]
                required_items['Good Will'] = curr_yr_good_will
            except Exception:
                print("Missing goodwill")
        if ('Intangible Assets' in balance_sheet_df.columns):
            try:
                intangible_assets_data = balance_sheet_df.loc[:,'Intangible Assets']
                curr_yr_intangible_asset = intangible_assets_data[0]
                required_items['Intangible Assets'] = curr_yr_intangible_asset
            except Exception:
                print("Missing intangible assets")
        df = pd.DataFrame(data=list(required_items.values())).T
        df.to_excel(writer,sheet_name = "Sheet 1", startrow=startrow,startcol=0, header=False,index=False)
        startrow += 1
        print("\n")
    except Exception as error:
        print(error)
        print("  Something went wrong with this stock, skipping it\n")
        continue

print("---ITEM 1 FINISHED---\n")          
writer.save()

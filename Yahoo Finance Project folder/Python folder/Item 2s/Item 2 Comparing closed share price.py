##To install the API, use
##pip install requests
##pip install pandas
##pip install bs4
##pip install yfinance
#-------------------------------------
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
import yfinance as yf
#-------------------------------------

#|----------------------------------------------------------------|
#|1. Can we download from yahoo finance the full list of stocks by|
#|market e.g. Singapore, US, Hong Kong, Japan, China?             |
#|Example with Singapore max                                      |
#|----------------------------------------------------------------|

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
    print("METHOD FINISHED")
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


#|--------------------------------------------------------------------------------------------------------------------|
#|2. Can we screen and download from yahoo finance the list of stocks that have closing share price fluctuating within|
#|range of (a) 5%, (b) 10%, (c) 20%, (d) 2% to 20% for the last (i) 5 days, (ii) 10 days, (iii) 20 days, (iv) 50 days |
#|by market e.g. Singapore, US, Hong Kong, Japan, China?                                                              |  
#|--------------------------------------------------------------------------------------------------------------------|

##------------------------------------------------------------------------------------------------------------------
## This section is meant to just copy over the stocks data into an excel file so that I can use yfinance to extract
## the market data of the stocks. 2 files will be created both named stocklist, the files can be deleted afterwards.
##------------------------------------------------------------------------------------------------------------------

newFilePath = r'C:\Users\nicky\OneDrive\Desktop\stocklist.xlsx'
tickers = pd.read_excel(newFilePath)

##----------------------------------------------------------------------------------------------------------------
## The file will be saved in an excel file under the name Output, or whatever name you wish it to be.
##----------------------------------------------------------------------------------------------------------------
yf.pdr_override()
newFile=r'C:\Users\nicky\OneDrive\Desktop\Output2.xlsx'
writer = pd.ExcelWriter(newFile, engine="xlsxwriter")
startrow=1

##----------------------------------------------------------------------------------------------------------------
## Here you can change the name of the headers
##----------------------------------------------------------------------------------------------------------------
headers = pd.DataFrame(columns=['Stock', 'Name', "Max_Price", "Min_Price", "Other_Endpoint", "Day_Zero_Data"
                                              ,"Period 5","Period 10","Period 20", "Period 50",
                                              "5%","10%","20%","2-20%"])

##-------------------------------------------------------------------------------------------------------------------
## Here you can change the name of the sheet. But make sure it matches the one below, I will make a comment above it.
##-------------------------------------------------------------------------------------------------------------------
headers.to_excel(writer,'Sheet 1')

#VERSION 1, SINGLE SHEET (BASICALLY, THE DESIRED VERS)
for i in tickers.index: #[start:end]: 
    stock = str(tickers["Symbol"][i])
    name = str(tickers["Name"][i])
    print("STOCK:  "+stock, ", NAME:  "+name)    
    try:
         
        tickerData = yf.Ticker(stock)
        ##----------------------------------------------------
        ## It is possible to change the periods you want here.
        ##----------------------------------------------------
        list_of_periods = [5,10,20,50]
        is_within_5pc_to_20pc = False
        is_within_2pc_to_20pc = False
        for period in list_of_periods:
            df =  pd.DataFrame(columns=[stock, name, "Max_Price", "Min_Price", "Other_Endpoint", "Day_Zero_Data",
                                        "NA5","NA10","NA20","NA50","NA5P","NA10P","NA20P","NA220P"])
            period_data = tickerData.history(period=str(period) + 'd')['Close']
            data_from_otherEndPoint_to_dayNegOne = period_data[0:period_data.size - 1]
            OTHER_ENDPOINT = period_data[0]
            DAY_ZERO_DATA = period_data[period_data.size - 1]
            #-----------------------------------------------------------
            # Here, you can change the number of decimal places you want
            #-----------------------------------------------------------
            MAX_PRICE = round(data_from_otherEndPoint_to_dayNegOne.max(),3)
            MIN_PRICE = round(data_from_otherEndPoint_to_dayNegOne.min(),3)
            
            if DAY_ZERO_DATA == 0 and OTHER_ENDPOINT == 0:
                continue
            if (period_data.size < period):
                continue
            
            df = df.rename(columns={"Max_Price":MAX_PRICE})
            df = df.rename(columns={"Min_Price":MIN_PRICE})
            df = df.rename(columns={"Other_Endpoint":OTHER_ENDPOINT})
            df = df.rename(columns={"Day_Zero_Data":DAY_ZERO_DATA})
            is_within_5pc_to_20pc = False
            is_within_2pc_to_20pc = False
            
            for percentage in [0.05,0.10,0.20]:
                #min and max within +/- X% of DAY_ZERO_DATA
                #----------------------------------
                # Here you can change the formula.
                #----------------------------------
                if ((MAX_PRICE - DAY_ZERO_DATA)/DAY_ZERO_DATA <= percentage and (DAY_ZERO_DATA - MIN_PRICE)/DAY_ZERO_DATA <= percentage):            
                    #PERIODS
                    if (period == 5 and 'Y' not in str(df.iloc[:,[5]])):
                        df = df.rename(columns={"NA5":'Y'})
                    if (period == 10 and 'Y' not in str(df.iloc[:,[6]])):
                        df = df.rename(columns={"NA10":'Y'})
                    if (period == 20 and 'Y' not in str(df.iloc[:,[7]])):
                        df = df.rename(columns={"NA20":'Y'})
                    if (period == 50 and 'Y' not in str(df.iloc[:,[8]])):
                        df = df.rename(columns={"NA50":'Y'})
                    #PERCENTAGES
                    if (percentage == 0.05):
                        df = df.rename(columns={"NA5P":"Y"})
                    if (percentage == 0.1):
                        df = df.rename(columns={"NA10P":"Y"})
                    if (percentage == 0.2):
                        df = df.rename(columns={"NA20P":"Y"})
                    is_within_5pc_to_20pc = True
            #---------------------------------
            # Here you can change the formula
            #---------------------------------
            if ( 0.02 <= (MAX_PRICE - DAY_ZERO_DATA)/DAY_ZERO_DATA <= 0.20  and 0.02 <= (DAY_ZERO_DATA - MIN_PRICE)/DAY_ZERO_DATA <= 0.20):    
                #PERIODS
                if (period == 5 and 'Y' not in str(df.iloc[:,[5]])):
                    df = df.rename(columns={"NA5":'Y'})
                if (period == 10 and 'Y' not in str(df.iloc[:,[6]])):
                    df = df.rename(columns={"NA10":'Y'})
                if (period == 20 and 'Y' not in str(df.iloc[:,[7]])):
                    df = df.rename(columns={"NA20":'Y'})
                if (period == 50 and 'Y' not in str(df.iloc[:,[8]])):
                    df = df.rename(columns={"NA50":'Y'})
                df = df.rename(columns={"NA220P":'Y'})
                is_within_2pc_to_20pc = True
                
            if (is_within_5pc_to_20pc or is_within_2pc_to_20pc):
                #----------------------------------------------------------
                # If you change the sheet name above, change here as well
                #----------------------------------------------------------
                df.to_excel(writer,sheet_name="Sheet 1",startrow=startrow)
                startrow += 1
                continue
                             
        print("-----------------------------------")
    except Exception as error:
        print(error)
        continue

#VERSION 2, BY SHEETS (THIS VERSION SAVES THE DATA IN SHEETS OF DIFFERENT PERIODS)
##newFile=r'C:\Users\nicky\OneDrive\Desktop\Compare.xlsx'
##writer = pd.ExcelWriter(newFile, engine="xlsxwriter")
##list_of_periods = [5,10,20,50]
##exportList= pd.DataFrame(columns=['Stock', "MAX_PRICE", "MIN_PRICE", "OTHER_ENDPOINT", "DAY_ZERO_DATA","PERIOD","PERCENTAGE"])
##for period in list_of_periods:
##    startrow = 1
##    exportList.to_excel(writer,str(period) + ' days')
##    for i in tickers.index:
##        stock = str(tickers["Ticker"][i])
##        print("STOCK:  "+stock)
##        tickerData = yf.Ticker(stock)
##        try:
##            period_data = tickerData.history(period=str(period) + 'd')['Close']
##            if (period_data.size < period):
##                continue
##            data_from_otherEndPoint_to_dayNegOne = period_data[0:period_data.size - 1]
##            OTHER_ENDPOINT = period_data[0]
##            DAY_ZERO_DATA = period_data[period_data.size - 1]
##            if DAY_ZERO_DATA == 0 and OTHER_ENDPOINT == 0:
##                continue
##            MAX_PRICE = round(data_from_otherEndPoint_to_dayNegOne.max(),3)
##            MIN_PRICE = round(data_from_otherEndPoint_to_dayNegOne.min(),3)
####            is_within_5percent_to_20percent = False
####            is_within_2percent_to_20percent = False
##            for percentage in [0.05,0.10,0.20]:
##                #min and max within +/- X% of DAY_ZERO_DATA
##                if ( ((MAX_PRICE - DAY_ZERO_DATA)/DAY_ZERO_DATA <= percentage and (DAY_ZERO_DATA - MIN_PRICE)/DAY_ZERO_DATA <= percentage)
##                #min and max within +/- X% of OTHER_ENDPOINT
##                or ((MAX_PRICE - OTHER_ENDPOINT)/OTHER_ENDPOINT <= percentage and (DAY_ZERO_DATA - MIN_PRICE)/OTHER_ENDPOINT <= percentage)):
##                    newDf = pd.DataFrame(columns=[stock,MAX_PRICE,MIN_PRICE,OTHER_ENDPOINT,DAY_ZERO_DATA,period,percentage])
##                    newDf.to_excel(writer,sheet_name=str(period) + ' days',startrow=startrow,startcol=1,index=False)
##                    startrow += 1
##                        
##            if (( 0.02 <=(MAX_PRICE - DAY_ZERO_DATA)/DAY_ZERO_DATA <= 0.20  and 0.02 <= (DAY_ZERO_DATA - MIN_PRICE)/DAY_ZERO_DATA <= 0.20)
##            or ((0.02 <= MAX_PRICE - OTHER_ENDPOINT)/OTHER_ENDPOINT <= 0.20 and (DAY_ZERO_DATA - MIN_PRICE)/OTHER_ENDPOINT <= 0.20)):
##                newDf = pd.DataFrame(columns=[stock,MAX_PRICE,MIN_PRICE,OTHER_ENDPOINT,DAY_ZERO_DATA,period,'0.02 -> 0.20'])
##                newDf.to_excel(writer,sheet_name=str(period) + ' days',startrow=startrow,startcol=1,index=False)
##                startrow += 1
##
##            print("-----------------------------------")
##        except Exception as error:
##            print(error)
##            continue

writer.save()  

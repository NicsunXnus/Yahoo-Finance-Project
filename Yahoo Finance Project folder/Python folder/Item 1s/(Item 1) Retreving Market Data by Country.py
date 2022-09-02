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
    print("---Finished extracting stock symbols from this market---")
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

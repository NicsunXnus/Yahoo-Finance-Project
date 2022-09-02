
#-------------------------------------
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
import yfinance as yf
#-------------------------------------

#|-------------------------------------------------------------------|
#| 8. Can we screen and download from yahoo finance the stocks       |
#| that have price to earning (PE) that is between 1 to 40 and       |
#| forward earning per share (EPS) is more than EPS (TTM or trailing)|
#| by market e.g. Singapore, US, Hong Kong, Japan, China?            |
#|-------------------------------------------------------------------|
filePath = r'C:\Users\nicky\OneDrive\Desktop\stocklist.xlsx'
tickers = pd.read_excel(filePath)
newFile= r'C:\Users\nicky\OneDrive\Desktop\Output8.xlsx'
writer = pd.ExcelWriter(newFile, engine="xlsxwriter")
##----------------------------------------------------------------------------------------------------------------
## Here you can change the name of the headers
##----------------------------------------------------------------------------------------------------------------
headers = pd.DataFrame(columns=['Stock', 'Name', "Trailing PE", "Trailing EPS", "Forward Earning Per Share"])
##-------------------------------------------------------------------------------------------------------------------
## Here you can change the name of the sheet. But make sure it matches the one below, I will make a comment above it.
##-------------------------------------------------------------------------------------------------------------------
headers.to_excel(writer,'Sheet 1')
startrow = 1
for i in tickers.index:
    stock = str(tickers["Symbol"][i])
    name = str(tickers["Name"][i])
    print(i, " ","STOCK:  "+stock, ", NAME:  "+name)    
    try:
        tickerData = yf.Ticker(stock)
        trailingPE = tickerData.info["trailingPE"]
        trailingEps = tickerData.info["trailingEps"]
        forwardEps = tickerData.info["forwardEps"]
        print(trailingPE," ", trailingEps," ", forwardEps)
        
        is_trailingPE_between_1_to_40 = 1 <= trailingPE <= 40
        is_forwardEps_more_than_trailingEPS = forwardEps > trailingEps
        if (is_trailingPE_between_1_to_40 and is_forwardEps_more_than_trailingEPS):
            df =  pd.DataFrame(columns=[stock, name, trailingPE, trailingEps, forwardEps])
            df.to_excel(writer, sheet_name='Sheet 1',startrow=startrow)
            startrow += 1
    except Exception as error:
        print("Error: " + str(error))
        continue
print("---ITEM 8 FINISHED---")
writer.save()

import yfinance as yf
import yahoo_fin.stock_info as si
import pandas as pd
import datetime as dt
import os
from pandas_datareader import data as pdr
from pandas import ExcelWriter

##
#The information to be downloaded includes:
#symbol, company name, last price, change, change %, day low, day high,
#52 weeks low, 52 weeks high,
#10 days moving average of share price, 20 days moving average of share price,
#50 days moving average of share price, 100 days moving average of share price,
#150 days moving average of share price, 200 days moving average of share price,
#target low price, target median price, target mean price, target high price,
#volume, average daily volume (10days), average daily volume (30days), average daily volume (3months),
#volume weighted average price, market capitalisation, enterprise value, trailing price to earning (PE),
#forward PE, PEG ratio, price to book value, price to revenue, EBITDA, earning per share (EPS) (TTM or trailing),
#EPS est. next year or forward EPS, dividend/share, trailing annual dividend yield, forward annual dividend yield,
#dividend payment date, ex-dividend date, current year revenue, previous year revenue, revenue growth (yearly),
#revenue per share, current year net income (applicable to common shares), previous year net income, current year EBITDA,
#previous year EBITDA, current year extraordinary items, previous year extraordinary items, current quarter revenue,
#previous quarter revenue, revenue growth (quarter), current quarter net income (applicable to common shares),
#previous quarter net income, current quarter EBITDA, previous quarter EBITDA, current quarter extraordinary items,
#previous quarter extraordinary items, cash, debt (short term + long term), book value, intangible assets,
#goodwill, cash per share, gross margin, EBITDA margin, profit margin,  % held by insiders (heldPercentInsiders),
#% held by Instititutions (heldPercentInstitutions), % of short vs float (shortpercentoffloat),
#earnings date, exchange, industry, sector, financial currency


##
yf.pdr_override()
##
#1. Can we download from yahoo finance the full list of stocks by
#market e.g. Singapore, US, Hong Kong, Japan, China?
##Example with Singapore market
##SG_stock_list_filepath = r'C:\Users\nicky\OneDrive\Desktop\Stocks_Excel\Singapore_stocks.xlsx'
##SG_stocklist = pd.read_excel(SG_stock_list_filepath)
##stocklist = [] ##create an empty container for the stocks
##for i in SG_stocklist.index:
##    stock=str(SG_stocklist["Symbol"][i])
##    stocklist.append(stock)
##    ##at the end, all the stock names will be added to the stocklist
##newFile=os.path.dirname(SG_stock_list_filepath)+"/SingaporeStockData.xlsx"
##writer= ExcelWriter(newFile)
##try:
##    df = yf.download(stocklist, group_by='Ticker', period='1y')
##    df = df.stack(level=0).rename_axis(['Date', 'Ticker']).reset_index(level=1)
##    df.to_excel(writer,"Sheet1")
##    writer.save()
##except Exception as error:
##    print("")
    
##

##
#2. Can we screen and download from yahoo finance the list of stocks that
#have closing share price fluctuating within a range (Me - ???) of
#(a) 5%, (b) 10%, (c) 20%, (d) 2% to 20% for the last
#(i) 5 days, (ii) 10 days, (iii) 20 days, (iv) 50 days
#by market e.g. Singapore, US, Hong Kong, Japan, China?
tickerData = yf.Ticker("AAPL")
#print(tickerData.financials)
msft_data = si.get_quote_table("MSFT")
print(msft_data)
todayData = tickerData.history(period='3d')
#print(type(todayData))
#print(todayData)
print("========================")
print(round(todayData['Close'].max(),2)) ##!!!!!Compare using closing price or also highs and lows???
##create tickers for all the stocks
#for i in stocklist:
 #   print("stock: ",i)
  #  try:
   #     tickerData = yf.Ticker(i)
    #    todayData = tickerData.history(period='10d')
        #lastClosingData = todayData['Close'][0]
        #print(lastClosingData)
     #   print(todayData)
      #  break
    #except Exception as error:
     #   continue

##

##TIME RANGE    
#start = dt.datetime(2010, 3, 9) #Y,M,D,MIN,SEC,MILLI SEC
#end = dt.datetime(2010, 3, 12)
#print(end - start)
##

##
#3. Can we screen and download from yahoo finance the list of stocks
#that have 10 days moving average of share price, 20 days moving average
#of share price, 50 days moving average of share price,
#100 days moving average of share price, 150 days moving average of share price,
#200 days moving average of share price are within a range of
#(a) 5%, (b) 10%, (c) 20%, (d) 2% to 20% from each other for the
#last (i) 5 days, (ii) 10 days, (iii) 20 days, (iv) 50 days by market
#e.g. Singapore, US, Hong Kong, Japan, China?
#(note: ie the 10 to 200 days moving average are close to each other)

#newFile=os.path.dirname(SG_stock_list_filepath)+"/ScreenOutput.xlsx"
#writer= ExcelWriter(newFile)
#for i in stocklist:    
 #   try:
  #      tickerData = yf.Ticker(i)
   #     df = tickerData.history(period='2y')[['Open', 'High', 'Low', 'Close', 'Volume']]
    #    smaUsed=[10,20,50,100,150,200]  
     #   for x in smaUsed:
      #      sma=x
       #     df["SMA_"+str(sma)]=round( df['Close'].rolling(window=sma).mean(),2)
        #lastClosingData = todayData['Close'][0]
        #print(lastClosingData)        
        #df.to_excel(writer,i)
        #writer.save()
    #except Exception as error:
     #   print(error)
      #  continue

##

##
#4. Can we screen and download from yahoo finance the list of stocks
#that have average closing share price during the last 5 days that is 2% to 20% above the
#last (i) 5 days, (ii) 10 days, (iii) 20 days, (iv) 50 days, (v) 200 days average closing price
#by market e.g. Singapore, US, Hong Kong, Japan, China?

##OK

##

##
#5. Can we screen and download from yahoo finance the list of stocks that have
#average closing share price during the last 5 days that is 2% to 20% below the
#last (i) 5 days, (ii) 10 days, (iii) 20 days, (iv) 50 days, (v) 200 days average closing price
#by market e.g. Singapore, US, Hong Kong, Japan, China?

##SAME AS Q4 but opposite


##

##
#6. Can we screen and download from yahoo finance the list of stocks that have average closing share price
#range/fluctuation/volatility during the last 10 days (Current Day to Day -9) that is less than the
#average closing price range/fluctuation/volatility during the earlier 10 days (Day -10 to -19)
#by market e.g. Singapore, US, Hong Kong, Japan, China?
#(note: ie the average last 10 days (Current Day to Day -9) price movement is within e.g. 3%
#compared to the earlier average 10 days (Day -10 to -19) with price movement of e.g. 8%,
#so the last 10 days average closing price is narrower than the earlier 10 days average closing price)

##

##
#7. Can we screen and download from yahoo finance the list of stocks that have average volume during the
#(i) last 5 days (Current Day to Day -4) that is higher the previous 5 days (Day -5 to Day -9),
#(ii) last 10 days (Current Day to Day -9) higher than previous 10 days (Day -10 to -19)

##OK. yfinance.info() -> already has average volume data

##

##
#8. Can we screen and download from yahoo finance the stocks that have price to earning (PE) that is
#between 1 to 40 and forward earning per share (EPS) is more than EPS (TTM or trailing)
#by market e.g. Singapore, US, Hong Kong, Japan, China? 

##yfinance,info() -> alreayd has trailing EPS and forward EPS

##

##

##

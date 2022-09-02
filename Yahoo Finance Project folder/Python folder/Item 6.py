#-------------------------------------
import pandas as pd
import yfinance as yf
#-------------------------------------

# 6. Can we screen and download from yahoo finance the list of stocks
# that have average closing share price range/fluctuation/volatility
# during the last 10 days (Current Day to Day -9) that is less than
# the average closing price range/fluctuation/volatility during the
# earlier 10 days (Day -10 to -19) by market
# e.g. Singapore, US, Hong Kong, Japan, China?
# (note: ie the average last 10 days (Current Day to Day -9) price movement is
# within e.g. 3% compared to the earlier average 10 days (Day -10 to -19)
# with price movement of e.g. 8%, so the last 10 days average closing price
# is narrower than the earlier 10 days average closing price)

newFilePath = r'C:\Users\nicky\OneDrive\Desktop\stocklist.xlsx'
tickers = pd.read_excel(newFilePath)

yf.pdr_override()
newFile=r'C:\Users\nicky\OneDrive\Desktop\Output6.xlsx'
writer = pd.ExcelWriter(newFile, engine="xlsxwriter")
startrow=1
headers = pd.DataFrame(columns=['Stock', 'Name', "Avg_closing_share_price_day0_to_dayNegNine", "Last_10_days_fluctuation",
                                "Avg_closing_share_price_dayNegTen_to_dayNegNineteen", "Earlier_10_days_fluctuation"])

headers.to_excel(writer,'Sheet 1')

for i in tickers.index:
    stock = str(tickers["Symbol"][i])
    name = str(tickers["Name"][i])
    print(i," ","STOCK:  "+stock, ", NAME:  "+name)    
    try:         
        tickerData = yf.Ticker(stock)
        twenty_day_period_data = tickerData.history(period="20d")["Close"]
        if (twenty_day_period_data.size < 20):
            print("-----------------------------------")
            continue
        last_ten_days_avg_closing_price = round(twenty_day_period_data[10:20].mean(), 3)
        #Lets calculate the fluctuation for the last ten days
        max_price_last_ten_days = round(max(twenty_day_period_data[10:20]),3)
        min_price_last_ten_days = round(min(twenty_day_period_data[10:20]),3)
        difference_betw_max_and_avg_last_ten_days = max_price_last_ten_days - last_ten_days_avg_closing_price
        difference_betw_avg_and_min_last_ten_days = last_ten_days_avg_closing_price - min_price_last_ten_days

        fluctuation_last_ten_days = 0
        if (difference_betw_max_and_avg_last_ten_days >= difference_betw_avg_and_min_last_ten_days):
            fluctuation_last_ten_days = difference_betw_max_and_avg_last_ten_days/last_ten_days_avg_closing_price
        elif (difference_betw_max_and_avg_last_ten_days < difference_betw_avg_and_min_last_ten_days):
            fluctuation_last_ten_days = difference_betw_avg_and_min_last_ten_days/last_ten_days_avg_closing_price
        
        earlier_ten_days_avg_closing_price = round(twenty_day_period_data[0:10].mean(), 3)
        #Lets calculate the fluctuation for the earlier ten days
        max_price_earlier_ten_days = round(max(twenty_day_period_data[0:10]),3)
        min_price_earlier_ten_days = round(min(twenty_day_period_data[0:10]),3)
        difference_betw_max_and_avg_earlier_ten_days = max_price_earlier_ten_days - earlier_ten_days_avg_closing_price
        difference_betw_avg_and_min_earlier_ten_days = earlier_ten_days_avg_closing_price - min_price_earlier_ten_days

        fluctuation_earlier_ten_days = 0
        if (difference_betw_max_and_avg_earlier_ten_days >= difference_betw_avg_and_min_earlier_ten_days):
            fluctuation_earlier_ten_days = difference_betw_max_and_avg_earlier_ten_days/last_ten_days_avg_closing_price
        elif (difference_betw_max_and_avg_earlier_ten_days < difference_betw_avg_and_min_earlier_ten_days):
            fluctuation_earlier_ten_days = difference_betw_avg_and_min_earlier_ten_days/last_ten_days_avg_closing_price

        if (fluctuation_last_ten_days < fluctuation_earlier_ten_days):
            print("-----------------------------------")
            df = pd.DataFrame(columns=[stock, name, last_ten_days_avg_closing_price,round(fluctuation_last_ten_days,3),
                                       earlier_ten_days_avg_closing_price, round(fluctuation_earlier_ten_days,3)])
            df.to_excel(writer,sheet_name="Sheet 1",startrow=startrow)
            startrow += 1
            continue
    except Exception as error:
        print(error)
        continue
print("---ITEM 6 FINISHED---")
writer.save()

#-------------------------------------
import pandas as pd
import yfinance as yf
#-------------------------------------


# 4. Can we screen and download from yahoo finance the list of stocks that have
# average closing share price during the last 5 days that is 2% to 20% below the last
# (i) 10 days, (ii) 20 days, (iii) 50 days, (iv) 200 days average closing price
# by market e.g. Singapore, US, Hong Kong, Japan, China?

newFilePath = r'C:\Users\nicky\OneDrive\Desktop\stocklist.xlsx'
tickers = pd.read_excel(newFilePath)

yf.pdr_override()
newFile=r'C:\Users\nicky\OneDrive\Desktop\Output5.xlsx'
writer = pd.ExcelWriter(newFile, engine="xlsxwriter")
startrow=1
headers = pd.DataFrame(columns=['Stock', 'Name', "Last 5 days avg closing price",
                                "Is 2% to 20% below last 10 Days",
                                "Is 2% to 20% below last 20 Days",
                                "Is 2% to 20% below last 50 Days",
                                "Is 2% to 20% below last 200 Days"])
headers.to_excel(writer,'Sheet 1')
#VERSION 1, SINGLE SHEET
for i in tickers.index[:10]:
    stock = str(tickers["Symbol"][i])
    name = str(tickers["Name"][i])
    print(i," ","STOCK:  "+stock, ", NAME:  "+name)
    tickerData = yf.Ticker(stock)
    five_day_period_data = tickerData.history(period=str('5d'))['Close']
    if (five_day_period_data.size < 5):
        continue
    condition_fulfilled = False
    last_5_days_avg_price = round(five_day_period_data.mean(), 3)
    df =  pd.DataFrame(columns=[stock, name,
                                        "Last 5 days avg closing price",
                                        "NA10",
                                        "NA20",
                                        "NA50",
                                        "NA200"])
    try:                
        list_of_periods = [10,20,50,200]
        for period in list_of_periods:
            period_data = tickerData.history(period=str(period) + 'd')['Close']
            if (period_data.size < period):
                print("-----------------------------------")
                continue
            avg_closing_price_for_period = round(period_data.mean(), 3)
            difference = last_5_days_avg_price - avg_closing_price_for_period
            percentage_difference = difference/avg_closing_price_for_period
            if (-0.2 <= percentage_difference <= -0.02):
                df = df.rename(columns={"NA" + str(period): "Y", "Last 5 days avg closing price":last_5_days_avg_price})
                if (not condition_fulfilled):
                    condition_fulfilled = True
        if (condition_fulfilled):            
            for label in ["NA10",
                                "NA20",
                                    "NA50",
                                        "NA200"]:
                if (label in list(df.columns)):
                    df = df.rename(columns={label:"-"})
            df.to_excel(writer,sheet_name="Sheet 1",startrow=startrow)
            startrow += 1
            print("-----------------------------------")
            continue
        print("-----------------------------------")
    except Exception as error:
        print(error)
        continue
print("---ITEM 5 FINISHED---")
writer.save()

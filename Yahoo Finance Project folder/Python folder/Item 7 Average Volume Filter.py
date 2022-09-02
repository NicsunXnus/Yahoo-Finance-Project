
#-------------------------------------
import pandas as pd
import yfinance as yf
#-------------------------------------

# 7. Can we screen and download from yahoo finance the list of stocks that have average volume
# during the (i) last 5 days (Current Day to Day -4) that is higher the previous 5 days (Day -5 to Day -9),
# (ii) last 10 days (Current Day to Day -9) higher than previous 10 days (Day -10 to -19)

newFilePath = r'C:\Users\nicky\OneDrive\Desktop\stocklist.xlsx'
tickers = pd.read_excel(newFilePath)

yf.pdr_override()
newFile=r'C:\Users\nicky\OneDrive\Desktop\Output7.xlsx'
writer = pd.ExcelWriter(newFile, engine="xlsxwriter")
startrow=1
headers = pd.DataFrame(columns=['Stock', 'Name', "Avg_Volume from day 0 to day -4", "Avg_Volume from day -5 to day -9",
                                "Avg_Volume from day 0 to day -9", "Avg_Volume from day -10 to day -19",
                                "(i) fulfilled", "(ii) fulfilled"])

headers.to_excel(writer,'Sheet 1')
#VERSION 1, SINGLE SHEET
for i in tickers.index[:10]:
    stock = str(tickers["Symbol"][i])
    name = str(tickers["Name"][i])
    print(i, " ","STOCK:  "+stock, ", NAME:  "+name)    
    try:        
        tickerData = yf.Ticker(stock)
        list_of_periods = [10,20]
        condition_1_fulfilled = False
        condition_2_fulfilled = False
        for period in list_of_periods:
            df =  pd.DataFrame(columns=[stock, name, "AV_ZERO_TO_NEGFOUR", "AV_NEGFIVE_TO_NEGNINE", "AV_ZERO_TO_NEGNINE", "AV_NEGTEN_TO_NEGNINETEEN",
                                        "NA5","NA10"])
            period_data = tickerData.history(period=str(period) + 'd')['Volume']
            if (period_data.size < period):
                continue
            if (period == 10):
                volume_betw_zero_to_negFour = period_data[5:10]
                volume_betw_negFive_to_negNine = period_data[0:5]
                AV_ZERO_TO_NEGFOUR = round(volume_betw_zero_to_negFour.mean(),3)
                AV_NEGFIVE_TO_NEGNINE = round(volume_betw_negFive_to_negNine.mean(),3)
                if (AV_ZERO_TO_NEGFOUR > AV_NEGFIVE_TO_NEGNINE):
                    condition_1_fulfilled = True
                    df = df.rename(columns={"AV_ZERO_TO_NEGFOUR":AV_ZERO_TO_NEGFOUR, "AV_NEGFIVE_TO_NEGNINE":AV_NEGFIVE_TO_NEGNINE,
                                            "NA5":"Y"})
            if (period == 20):
                volume_betw_zero_to_negNine = period_data[0:10]
                volume_betw_negTen_to_negNineteen = period_data[11:20]
                AV_ZERO_TO_NEGNINE = round(volume_betw_zero_to_negNine.mean(),3)
                AV_NEGTEN_TO_NEGNINETEEN = round(volume_betw_negTen_to_negNineteen.mean(),3)
                if (AV_ZERO_TO_NEGNINE > AV_NEGTEN_TO_NEGNINETEEN):
                    condition_2_fulfilled = True
                    df = df.rename(columns={"AV_ZERO_TO_NEGNINE":AV_ZERO_TO_NEGNINE, "AV_NEGTEN_TO_NEGNINETEEN":AV_NEGTEN_TO_NEGNINETEEN,
                                            "NA10":"Y"})
            if (condition_1_fulfilled or condition_2_fulfilled):
                for label in ["AV_ZERO_TO_NEGFOUR", "AV_NEGFIVE_TO_NEGNINE", "AV_ZERO_TO_NEGNINE",
                              "AV_NEGTEN_TO_NEGNINETEEN","NA5","NA10"]:
                    if (label in list(df.columns)):
                        df = df.rename(columns={label:"-"})
                df.to_excel(writer,sheet_name="Sheet 1",startrow=startrow)
                startrow += 1
                continue                             
        print("-----------------------------------")
    except Exception as error:
        print(error)
        continue
print("---ITEM 7 FINISHED---")
writer.save()

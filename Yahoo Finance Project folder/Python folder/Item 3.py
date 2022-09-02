#-------------------------------------
import pandas as pd
import yfinance as yf
#-------------------------------------

#|--------------------------------------------------------------------------------------------------------------------|
##
#3. Can we screen and download from yahoo finance the list of stocks
#that have 10 days moving average of share price, 20 days moving average
#of share price, 50 days moving average of share price,
#100 days moving average of share price, 150 days moving average of share price,
#200 days moving average of share price are within a range of
#(a) 5%, (b) 10%, (c) 20%, (d) 2% to 20% from each other for the
#last (i) 5 days, (ii) 10 days, (iii) 20 days, (iv) 50 days by market
#e.g. Singapore, US, Hong Kong, Japan, China?
#(note: ie the 10 to 200 days moving average are close to each other)                                                            |  
#|--------------------------------------------------------------------------------------------------------------------|

##------------------------------------------
##Data from the stocks in the excel file is read
##------------------------------------------

newFilePath = r'C:\Users\nicky\OneDrive\Desktop\stocklist.xlsx'
tickers = pd.read_excel(newFilePath)

##----------------------------------------------------------------------------------------------------------------
## The file will be saved in an excel file under the name Output, or whatever name you wish it to be.
##----------------------------------------------------------------------------------------------------------------
yf.pdr_override()
newFile=r'C:\Users\nicky\OneDrive\Desktop\Output3.xlsx'
writer = pd.ExcelWriter(newFile, engine="xlsxwriter")
startrow=2

##----------------------------------------------------------------------------------------------------------------
## Here you can change the name of the headers
##----------------------------------------------------------------------------------------------------------------
top_header = pd.DataFrame(columns=["10-200 days MA"] )
headers = pd.DataFrame(columns=['Stock Symbol', 'Name', "Period 5","Period 10","Period 20", "Period 50",
                                              "5%","10%","20%","2-20%"])

##-------------------------------------------------------------------------------------------------------------------
## Here you can change the name of the sheet. But make sure it matches the one below, there will be a comment above it.
##-------------------------------------------------------------------------------------------------------------------
top_header.to_excel(writer,sheet_name ="Sheet 1",startrow=0,startcol=3)
headers.to_excel(writer,sheet_name='Sheet 1',startrow=1)

#VERSION 1, SINGLE SHEET (BASICALLY, THE DESIRED VERS)
for i in tickers.index[:10]: 
    stock = str(tickers["Symbol"][i])
    name = str(tickers["Name"][i])
    print(i," ","STOCK:  "+stock, ", NAME:  "+name)    
    try:         
        tickerData = yf.Ticker(stock)
        ##----------------------------------------------------
        ## It is possible to change the periods you want here.
        ##----------------------------------------------------
        list_of_periods = [5,10,20,50]
        list_of_ma_range = [10,20,50,100,150,200]
        is_within_5pc_to_20pc = False
        is_within_2pc_to_20pc = False
        for period in list_of_periods:
            df =  pd.DataFrame(columns=[stock, name,
                                        "NA5","NA10","NA20","NA50","NA5P","NA10P","NA20P","NA220P"])
            
            for day in range(period): #check of each day within the period
                print("day: ",day)
                fluctuation_comparison = {}
                print("-----------------------------------")
                for ma_range in list_of_ma_range:
                    period_data = tickerData.history(period=str(ma_range + day) + 'd')['Close']
                    if (period_data.size <  ma_range + day):
                        print("Not enough data.\n")
                        break
                    moving_average_data = round(period_data[:ma_range].mean(),3)
                    fluctuation_comparison[str(ma_range) + " MA"] = moving_average_data
                print("-----------------------------------")    
                values = fluctuation_comparison.values()
                max_value = max(values)
                min_value = min(values)
                fluctuation = (max_value - min_value)/min_value

                is_within_5pc_to_20pc = False
                is_within_2pc_to_20pc = False
                for percentage in [0.05,0.10,0.20]:
                    if (fluctuation <= percentage):
                        if (period == 5 and 'Y' not in str(df.iloc[:,[3]])):
                            df = df.rename(columns={"NA5":'Y'})
                        if (period == 10 and 'Y' not in str(df.iloc[:,[4]])):
                            df = df.rename(columns={"NA10":'Y'})
                        if (period == 20 and 'Y' not in str(df.iloc[:,[5]])):
                            df = df.rename(columns={"NA20":'Y'})
                        if (period == 50 and 'Y' not in str(df.iloc[:,[6]])):
                            df = df.rename(columns={"NA50":'Y'})
                        #PERCENTAGES
                        if (percentage == 0.05):
                            df = df.rename(columns={"NA5P":"Y"})
                        if (percentage == 0.1):
                            df = df.rename(columns={"NA10P":"Y"})
                        if (percentage == 0.2):
                            df = df.rename(columns={"NA20P":"Y"})
                        is_within_5pc_to_20pc = True
                if (0.02 <= fluctuation <= 0.2):
                    if (period == 5 and 'Y' not in str(df.iloc[:,[3]])):
                        df = df.rename(columns={"NA5":'Y'})
                    if (period == 10 and 'Y' not in str(df.iloc[:,[4]])):
                        df = df.rename(columns={"NA10":'Y'})
                    if (period == 20 and 'Y' not in str(df.iloc[:,[5]])):
                        df = df.rename(columns={"NA20":'Y'})
                    if (period == 50 and 'Y' not in str(df.iloc[:,[6]])):
                        df = df.rename(columns={"NA50":'Y'})
                    df = df.rename(columns={"NA220P":'Y'})
                    is_within_2pc_to_20pc = True
                
                if (is_within_5pc_to_20pc or is_within_2pc_to_20pc):
                    #----------------------------------------------------------
                    # If you change the sheet name above, change here as well
                    #----------------------------------------------------------
                    df.to_excel(writer,sheet_name="Sheet 1",startrow=startrow)
                    startrow += 1
                    #continue to next period as already found within
                    break
        print("-----------------------------------")
    except Exception as error:
        print(error)
        continue
print("---ITEM 3 FINISHED---")   
writer.save()                

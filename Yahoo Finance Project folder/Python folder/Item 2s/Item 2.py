
#-------------------------------------
import pandas as pd
import yfinance as yf
#-------------------------------------

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
    print(i, " ","STOCK:  "+stock, ", NAME:  "+name)    
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
            period_data = tickerData.history(period=str(period + 1) + 'd')['Close']
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
                if (DAY_ZERO_DATA <= MAX_PRICE <= (1 + percentage) * DAY_ZERO_DATA and (1 -percentage) * DAY_ZERO_DATA <= MIN_PRICE <= DAY_ZERO_DATA):            
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
            if ( (DAY_ZERO_DATA <= MAX_PRICE <= 1.02 * DAY_ZERO_DATA and 0.98 * DAY_ZERO_DATA <= MIN_PRICE <= DAY_ZERO_DATA)
                 and (DAY_ZERO_DATA <= MAX_PRICE <= 1.2 * DAY_ZERO_DATA and 0.8 * DAY_ZERO_DATA <= MIN_PRICE <= DAY_ZERO_DATA)):    
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
                for label in ["NA5","NA10","NA20","NA50","NA5P","NA10P","NA20P","NA220P"]:
                    if (label in list(df.columns)):
                        df = df.rename(columns={label:"-"})
                df.to_excel(writer,sheet_name="Sheet 1",startrow=startrow)
                startrow += 1
                continue
                             
        print("-----------------------------------")
    except Exception as error:
        print("Something went wrong with the stock! Skipping it.")
        continue
print("---ITEM 2 FINISHED---")
writer.save() 

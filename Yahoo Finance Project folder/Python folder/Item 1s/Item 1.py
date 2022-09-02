import yfinance as yf
import yahoo_fin.stock_info as si
import pandas as pd

# Note, will take quite a while
def item_1(stock_list_excel_data_filePath):
    try:
        tickers = pd.read_excel(stock_list_excel_data_filePath)
    except Exception:
        print("Something went wrong with the file path, please try again.")

    yf.pdr_override()
    # Where the data will be stored at
    newFile = r'C:\Users\nicky\OneDrive\Desktop\Output1.xlsx'
    writer = pd.ExcelWriter(newFile, engine="xlsxwriter")
    startrow = 0
    are_headers_there = False
    for i in tickers.index[:30]: #here you can control how many stocks you want to read. You can remove the whole bracket if you want to get everything
        stock = str(tickers["Symbol"][i])
        name = str(tickers["Name"][i])
        print(i, " ",stock, " ",name)
        try:
            stats_df = si.get_stats(stock).T.reset_index(drop=True)
                
            balance_sheet_df = si.get_balance_sheet(stock).iloc[:,:1].T.reset_index(drop=True)
            balance_sheet_df = balance_sheet_df.columns.to_frame().T.append(balance_sheet_df, ignore_index=True)
            balance_sheet_df.columns = range(len(balance_sheet_df.columns))
           
            cash_flow_df = si.get_cash_flow(stock).iloc[:,:1].T.reset_index(drop=True)
            cash_flow_df = cash_flow_df.columns.to_frame().T.append(cash_flow_df, ignore_index=True)
            cash_flow_df.columns = range(len(cash_flow_df.columns))

            income_statement_df = si.get_income_statement(stock).iloc[:,:1].T.reset_index(drop=True)
            income_statement_df = income_statement_df.columns.to_frame().T.append(income_statement_df, ignore_index=True)
            income_statement_df.columns = range(len(income_statement_df.columns))

            major_holders_df = si.get_holders(stock)['Major Holders'].T
            #swap row 0 and row 1
            b, c = major_holders_df.iloc[0].copy(), major_holders_df.iloc[1].copy()
            major_holders_df.iloc[0],major_holders_df.iloc[1] = c,b

            dataFrames = [stats_df,balance_sheet_df,cash_flow_df,income_statement_df,major_holders_df]
            combined_df = pd.concat(dataFrames, axis=1)
            combined_df.insert(0,'0', ["Symbol",stock])
            combined_df.insert(1,'1', ["Name",name])
            combined_df.columns = combined_df.iloc[0]
            combined_df = combined_df.drop(0)
            combined_df.to_excel(writer, sheet_name="Sheet 1",startrow=startrow,index=False)
            startrow += 2

        except Exception as error:
            print("  Something went wrong with this stock, skipping it")
            continue
    print("---ITEM 1 FINISHED---")          
    writer.save()

from finviz.screener import Screener

##
yf.pdr_override()
##
#1. Can we download from yahoo finance the full list of stocks by
#market e.g. Singapore, US, Hong Kong, Japan, China?
##Example with Singapore market

##Screener used: https://finviz.com/screener.ashx?v=141&f=geo_usa&o=price

filters = ['USA']  # Type in the country you want to filter the MARKET
                   # DATA from
#Below is an example of how you can change what type of data you want to see.
# For more information on what inputs you can enter into table and order, please
# refer to the link to the Screener above.
stock_list = Screener(filters=filters,rows=100, table='Performance', order='price')  # Get the performance table and sort it by price ascending
print(type(stock_list))
print(stock_list)   
##

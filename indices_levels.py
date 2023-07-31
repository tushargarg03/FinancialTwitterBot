import yahoo_fin.stock_info as si
import tweet

# price_INDEX returns the current price of the specified index while change_INDEX
# returns the percent change of that index

def price_sp500():
    data = si.get_live_price("^GSPC")
    return round(data,2)

def price_nasdaq():
    data = si.get_live_price("^DJI")
    return round(data,2)

def price_dow():
    data = si.get_live_price("^IXIC")
    return round(data,2)

def change_sp500():
    data = si.get_data("^GSPC")  
    curr = price_sp500()
    prev = data['close'][-2]  
    
    change = (curr - prev) / prev * 100
    
    return round(change,2)

def change_nasdaq():
    data = si.get_data("^DJI")  
    curr = price_nasdaq()
    prev = data['close'][-2]  
    
    change = (curr - prev) / prev * 100
    
    return round(change,2)

def change_dow(): 
    data = si.get_data("^IXIC")
    curr = price_dow()
    prev = data['close'][-2]  
    
    change = (curr - prev) / prev * 100
    
    return round(change,2)

#returns the string of the indices level for the tweet
def make_tweet():
    result = "Indices Levels:\n"
    result += "$SPX -->  " + str(price_sp500()) + " (" + str(change_sp500()) + "%)\n" 
    result += "$NDX -->  " + str(price_nasdaq()) + " (" + str(change_nasdaq()) + "%)\n"
    result += "$DJI -->  " + str(price_dow()) + " (" + str(change_dow()) + "%)"

    return result

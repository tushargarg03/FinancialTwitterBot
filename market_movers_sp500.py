import yahoo_fin.stock_info as si
import tweet
import datetime

def market_gainers():
    data = si.get_day_gainers().head(5)

    result = "Largest Gains 📈:\n" 

    for i in range(5):
        result += "$" + data.iloc[i][0] + " -> " + str(data.iloc[i][4]) +'%\n'

    return result

def market_losers():
    data = si.get_day_losers().head(5)

    result = "Largest Losses 📉:\n" #maybe add in the time of tweet or something

    for i in range(5):
        result += "$" + data.iloc[i][0] + " -> " + str(data.iloc[i][4]) +'%\n'

    return result
    
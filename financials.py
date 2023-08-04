import yahoo_fin.stock_info as si
import yfinance as yf
import meaningcloud
import tweet
import datetime

#indices levels
sp500 = round(si.get_live_price("^GSPC"),2)
nasdaq = round(si.get_live_price("^IXIC"),2)
dow = round(si.get_live_price("^DJI"),2)

def market_gainers():
    data = si.get_day_gainers().head(5)

    result = "Largest Gains 📈:\n" 

    for i in range(5):
        result += f'${data.iloc[i][0]}  ->  {data.iloc[i][4]} %\n'

    return result

def market_losers():
    data = si.get_day_losers().head(5)

    result = "Largest Losses 📉:\n" #maybe add in the time of tweet or something

    for i in range(5):
         result += f'${data.iloc[i][0]}  ->  {data.iloc[i][4]} %\n'

    return result

tweet.tweet(market_losers())
    
#returns the string of the indices level and the changes for the tweet
def indices_update():
    result = "Indices Levels:\n"
    sp500_change = round((sp500 - si.get_data("^GSPC")['close'][-2]) / si.get_data("^GSPC")['close'][-2] * 100,2)
    nasdaq_change = round((nasdaq - si.get_data("^IXIC")['close'][-2]) / si.get_data("^IXIC")['close'][-2] * 100,2)
    dow_change = round((dow - si.get_data("^DJI")['close'][-2]) / si.get_data("^DJI")['close'][-2] * 100,2)

    result += f"$SPX -->  {sp500} ({sp500_change}%)\n" 
    result += f"$NDX -->  {nasdaq} ({nasdaq_change}%)\n" 
    result += f"$DJI -->  {dow} ({dow_change}%)\n" 

    return result

#returns the string for the company overview 
def company_gen_info(company_ticker: str):
    result = ""
   
    company = yf.Ticker(company_ticker[1:])
    all_data = company.info

    #general data
    result +=  company_ticker +  " -> " + all_data.get("shortName") +"\n"
    result += "Industry: " + all_data.get("industry") + "\n"
    result += "Sector: " + all_data.get("sector") + "\n"

    #make this into own function for company overview
    #result += summarizer(all_data.get("longBusinessSummary"), 1) + "\n"

    #financials begin here
    result += "\nRevenue: $" + format_financials(all_data.get("totalRevenue")) + "\n"
    result += "$" + str(all_data.get("currentPrice")) + "/share -> " + format_financials(all_data.get("marketCap")) + " Market Cap\n"
    result += "Avg. Volume: " + format_financials(all_data.get("averageVolume"))
    
    #dividend checker
    if all_data.get("dividendYield") is not None:
        result += "\nDividend Yield: " + str(all_data.get("dividendYield") * 100) + "%"

    return result

#returns the string for ^ quick summary of what the company does- try to figure out how we can reply
#to our own tweet to combine the two when the time comes!
def company_summarizer(company_ticker: str):
    text = yf.Ticker(company_ticker[1:]).info.get("longBusinessSummary")
        
    return company_ticker + "\n" + summarizer(text, 1)
       
#helper function to evaluate financial formatting
def format_financials(number: int):

    if number == None:
        return "Unable to calculate"

    if number >= 1000000000000:
        number /= 1000000000000
        return str("{:.2f}".format(number)) + "T"
    elif number < 1000000000000 and number >=1000000000:
        number /= 1000000000
        return str("{:.2f}".format(number)) + "B"
    elif number >= 1000000 and number < 1000000000:
        number /= 1000000
        return str("{:.2f}".format(number)) + "M"
    elif number >= 1000 and number <= 1000000:
        number /= 1000
        return str("{:.2f}".format(number)) + "K"
    else:
        return str(number)

#using meaningcloud api, this summarizes the text into the number of sentences asked
def summarizer(text: str, sent_count: int):
    if text == None or sent_count <= 0:
        return None

    license_key = '850273e65344d5b390b42477a65b5d69'

    text_summarized = meaningcloud.SummarizationResponse(meaningcloud.SummarizationRequest(key= license_key, txt= text, sentences= sent_count).sendReq())

    return text_summarized.getSummary()
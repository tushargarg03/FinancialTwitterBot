import yahoo_fin.stock_info as si
import yfinance as yf
import meaningcloud

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
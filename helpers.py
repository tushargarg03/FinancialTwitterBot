


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
import tweepy

client = tweepy.Client(
    bearer_token= 'AAAAAAAAAAAAAAAAAAAAAC3ZoAEAAAAAMSmY%2F09ii%2BNsqjTGN11VfY610t0%3D2BMoleZZI9bhBYOc8Nia2GwJ1LR9QOyUdcWWwn14xH38ORCkqx',
    consumer_key='XMhmSGnaz2fqdWjmEGOiI5G6X',
    consumer_secret='msvcyiv6SP1lCpC9iDm4p9gxKiUT9nmjT2t7PFaEyU1gJ7Gr1E',
    access_token='1669412065289617428-35KJKPnMkQuThXBXVggObKx7TttfGe',
    access_token_secret='SPLg2BJsM3pheCzEOkv4wMGWdA27IuH7KmBWeadNCzdDy'
)

#Takes in a string and tweets it out, basic for now but need to check for failures and stuff like that
def tweet(s: str):
    client.create_tweet(text= s)
    print("Tweet Successful!")
    #test again
    
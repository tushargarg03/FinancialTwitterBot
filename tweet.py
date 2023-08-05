import tweepy
import os
from dotenv import load_dotenv

load_dotenv()

#tweet functionality
client = tweepy.Client(
    bearer_token= os.getenv('bearer_token'), 
    consumer_key= os.getenv('consumer_key'),
    consumer_secret= os.getenv('consumer_secret'),
    access_token= os.getenv('access_token'),
    access_token_secret= os.getenv('access_token_secret')
)

#Takes in a string and tweets it out, basic for now but need to check for failures and stuff like that
def tweet(s: str):
    client.create_tweet(text= s)
    print("Tweet Successful!")

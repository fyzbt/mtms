import tweepy
import pandas as pd
from time import sleep

ACCESS_TOKEN = input("Insert the access token: ")
ACCESS_SECRET = input("Insert the secret token: ")
CONSUMER_KEY = input("Insert the consumer key: ")
CONSUMER_SECRET = input("Insert the consumer secret key: ")

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

RU = '@greenpeaceru'
EN = '@greenpeaceusa'
FR = '@greenpeacefr'
UK = '@GreenpeaceUK'
QUERIES = [RU, EN, FR, UK]


def get_tweets(queries, save=True, after="2018-01-01"):
    after = pd.to_datetime(after)
    for query in queries:
        print(f"Started collecting data for {query}")

        request = tweepy.Cursor(api.search, q=query + " -filter:retweets", lang='ru', tweet_mode='extended',
                                count=10000, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)\
                        .items(5000)
        print(len(request))
        data = [(status.author.name, status.created_at, status.full_text)
                for status in request if
                status.created_at > after]

        df = pd.DataFrame(data, columns=["username", "datetime", "text"])
        if save:
            df.to_csv(f"./data/twitter_data_{query}.csv")
            print(f"{query} data has {df.shape[0]} rows")
        else:
            return df

        sleep(5)

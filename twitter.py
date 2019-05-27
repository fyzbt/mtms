import tweepy
import pickle
from time import sleep

ACCESS_TOKEN = input("Insert the access: ")
ACCESS_SECRET = input("Insert the secret token: ")
CONSUMER_KEY = input("Insert the consumer key: ")
CONSUMER_SECRET = input("Insert the consumer secret key: ")

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)


GR_RU = 'greenpeaceru'
GR_USA = 'greenpeaceusa'
GR_FR = 'greenpeacefr'
GR_UK = '@GreenpeaceUK'
IDS = [GR_RU, GR_USA, GR_FR, GR_UK]


def get_all_tweets_of_acc(ids=IDS, max_num=10000):
    assert isinstance(ids, list)
    for account in ids:
        if account is GR_RU:
            tweets_lang = 'ru'
        if account is GR_USA:
            tweets_lang = 'en'
        if account is GR_FR:
            tweets_lang = 'fr'

        print(f"Start getting tweets from {account}")
        request = tweepy.Cursor(api.user_timeline, id=account, lang=tweets_lang,
                                tweet_mode='extended', count=max_num,
                                wait_on_rate_limit=True, wait_on_rate_limit_notify=True) \
                        .items()
        data = [(status.created_at, status.full_text) for status in request]

        with open(f"./data/twitter/{account}.pkl", 'wb') as f:
            pickle.dump(data, f)

        print(f"Tweets from {account} are successfully saved to {f}")

        sleep(2)


get_all_tweets_of_acc()

#! /usr/bin/env python
# -*- coding: utf-8 -*-

import random
import tweepy
from time import sleep
from creds import *


# Authenticating
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True) # to avoid the pesky 429 error code

queries = ["not the results we", "not the result we"]
max_rt = 200

# Time to tweet:
def main():
    count = 0
    for query in queries:
        for tweet in tweepy.Cursor(api.search, q = query, tweet_mode='extended').items(max_rt):
            try:
                text = tweet.retweeted_status.full_text.lower()
            except AttributeError:
                text = tweet.full_text.lower()
            if not tweet.retweeted:
                if "not the result we" in text or "not the results we" in text:
                    try:
                        tweet.retweet()
                        print("Retweeted %s" % tweet.user.screen_name)
                        count += 1
                    except tweepy.TweepError as e:
                        print(e.api_code, e.reason)
                        sleep(60 * 2)
                        continue
                    except StopIteration:
                        break
    print("Total retweets: %d" % count)


if __name__ == "__main__":
    main()
# Filename: reddit-scraper-inator.py  SRC: J.Coppens 2020

import praw
import pandas as pd
import config

SUBREDDIT = 'PrequelMemes'

reddit = praw.Reddit(client_id = config.PERSONAL_USE_SCRIPT, \
                     client_secret = config.SECRET_KEY, \
                     user_agent = 'reddit-scraper-inator', \
                     username = 'rocket-sheep', \
                     password = config.PASSWORD)

subreddit = reddit.subreddit(SUBREDDIT)

for submission in subreddit.top(limit=50):
    print(submission.title, submission.score)


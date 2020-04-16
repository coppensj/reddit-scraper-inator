# Filename: reddit-scraper-inator.py  SRC: J.Coppens 2020

import praw
import pandas as pd
import config
from PIL import Image
import urllib, io
import datetime as dt
import os

reddit = praw.Reddit(client_id = config.PERSONAL_USE_SCRIPT, \
                     client_secret = config.SECRET_KEY, \
                     user_agent = 'reddit-scraper-inator', \
                     username = 'rocket-sheep', \
                     password = config.PASSWORD)

thibbyboy = reddit.redditor('Thibson34')
title_string = 'Every day General Grievous adds a unique lightsaber to his collection.'

posts = {
        'date': [],
        'day': [],
        'description': [],
        'karma': [],
        # 'karma_ratio': [],
        'num_comments': [],
        'silv': [],
        'gold': [],
        'plat': [],
        'img_file': []}

if not os.path.exists('Images/'): os.makedirs('Images/')

for submission in thibbyboy.submissions.new(limit=200):
    if submission.subreddit not in ['PrequelMemes', 'HistoryMemes']:
        continue    
    if title_string not in submission.title:
        continue
    else:
        print(submission.title)
        title = submission.title.split('.')
        day = int(title[1].split(':')[0][5:7])
        posts['date'].append(dt.date.fromtimestamp(submission.created_utc))
        posts['day'].append(day)
        posts['description'].append(title[1].split(':')[1][1:])
        posts['karma'].append(submission.score)
        # posts['karma_ratio'].append(submission.upvote_ratio)
        posts['num_comments'].append(submission.num_comments)

        if 'gid_1' in submission.gildings.keys():
            posts['silv'].append(submission.gildings['gid_1'])
        else:
            posts['silv'].append(0)
        if 'gid_2' in submission.gildings.keys():
            posts['gold'].append(submission.gildings['gid_2'])
        else:
            posts['gold'].append(0)
        if 'gid_3' in submission.gildings.keys():
            posts['plat'].append(submission.gildings['gid_3'])
        else:
            posts['plat'].append(0)
        
        filename = f"Images/day_{day}.png"
        with urllib.request.urlopen(submission.url) as url:
            f = io.BytesIO(url.read())
        im = Image.open(f)
        im = im.convert('RGB')
        im.save(filename)
        posts['img_file'].append(filename)

posts = pd.DataFrame(posts).sort_values(by=['day'])
print(posts)
posts.to_csv(r'thibson34_grievous_post_data.csv')

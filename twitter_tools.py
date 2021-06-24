#!/usr/bin/env python
# coding: utf-8

import twitter
import random
import requests
from tools import load_credentials

CREDENTIALS = load_credentials()

def load_twitter_image(id,path):
    
    api = twitter.Api(consumer_key=CREDENTIALS['twitter']['api_key'],
                      consumer_secret=CREDENTIALS['twitter']['api_secret'],
                      access_token_key=CREDENTIALS['twitter']['access_token'],
                      access_token_secret=CREDENTIALS['twitter']['access_token_secret'])

    messages = api.GetUserTimeline(id)
    messages = [x for x in messages if x.media]
    img_url = random.sample(messages,1)[0].media[0].media_url
    r = requests.get(img_url, allow_redirects=True)
    f = open('resources/images/{}'.format(path),'wb')
    f.write(r.content)
    f.close()

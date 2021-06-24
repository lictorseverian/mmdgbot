#!/usr/bin/env python
# coding: utf-8

import yaml
import random

def prepare_google_link(text):

    googlefied = text.replace(' ','+')

    return '[{}](https://www.google.com/search?q={})'.format(text,googlefied)

def load_credentials():

    f = open('config/credentials.yaml','r')
    credentials = yaml.load(f)
    return credentials

def load_phrases(file,n=1):

    path = 'resources/text/{}'.format(file)
    f = open(path,'r',encoding='utf-8')
    filedata = f.read()
    phrases = filedata.split('\n')
    if n==1:
        return random.sample(phrases,n)[0].replace('<br>','\n')
    else:
        parsed_phrases = []
        phrases = random.sample(phrases,n)
        for p in phrases:
            parsed_phrases.append(p.replace('<br>','\n'))
        return parsed_phrases

#!/usr/bin/env python
# coding: utf-8

import os
import discord
import wikipedia
import datetime
import discord
import random
import twitter
import requests
from tools import load_credentials
from assigner import assign_response

CREDENTIALS = load_credentials()

client = discord.Client()

@client.event
async def on_ready():

    print(f'{client.user} is connected to the following guilds:\n')
    for guild in client.guilds:
        print(f'{guild.name}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    try:
        response, img = assign_response(message.content)

        if img:
            img = 'resources/images/{}'.format(img)
        if not response and not img:
            return
        elif response and not img:
            await message.channel.send(response)
        elif img and not response:
            await message.channel.send(file=discord.File(img))
        else:
            await message.channel.send(response, file=discord.File(img))
    except Exception as e:
        raise(e)
        response = 'I would prefer not to - {}'.format(e)
        await message.channel.send(response)

client.run(CREDENTIALS['discord']['bot_token'])
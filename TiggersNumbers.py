import os
from os.path import join, dirname
import tweepy
from random import *
from dotenv import load_dotenv
import discord
import asyncio
import datetime

# initialize Discord Client
client = discord.Client()

# load .env file
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# get environment variables
CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_KEY = os.environ.get('ACCESS_KEY')
ACCESS_SECRET = os.environ.get('ACCESS_SECRET')
CHANNEL_ID = os.environ.get('CHANNEL_ID')
DISCORD_KEY = os.environ.get('DISCORD_KEY')

# initialize Twitter Client
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

# get numbers
num1 = randint(1, 99)
num2 = randint(1, 99)

# ensure they're not the same number
while num1 == num2:
	num2 = randint(1, 99)

# format the numbers into strings
if(num1 < 10):
	num1string = "0" + str(num1)
else:
	num1string = str(num1)

if(num2 < 10):
        num2string = "0" + str(num2)
else:
        num2string = str(num2)

# write message
message = "Today's numbers are " + num1string + " and " + num2string

# send tweet
api.update_status(message)

# define discord function
@client.event
async def on_ready():
  await client.send_message(client.get_channel(CHANNEL_ID), message)
  await client.close()

# run discord function
client.run(DISCORD_KEY)

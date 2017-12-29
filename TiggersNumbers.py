import os
from os.path import join, dirname
import tweepy
from dotenv import load_dotenv
import discord
import asyncio
from datetime import date, datetime
from modules import db

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
numbers = db.get_numbers(datetime.now().replace(hour=0, minute=0, second=0, microsecond=0))
num1string = numbers[0][1]
num2string = numbers[0][2]

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

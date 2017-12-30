import os, sys
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
DISCORD_KEY = os.environ.get('DISCORD_KEY')

# initialize Twitter Client
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

# get numbers
numbers = db.get_numbers(datetime.now().replace(hour=0, minute=0, second=0, microsecond=0))
if(len(numbers) == 0):
    sys.exit()

num1string = numbers[0][1]
num2string = numbers[0][2]

# write message
message = "Today's numbers are " + num1string + " and " + num2string

# send tweet
api.update_status(message)

# define discord function
@client.event
async def on_ready():
    # get all channels
    channels = db.get_channels()
    if(len(channels) > 0):
        # loop through and send message to each channel
        for channel in channels:
            try:
                await client.send_message(client.get_channel(channel[0]), message)
            # if exception, remove channel from table
            except(discord.errors.InvalidArgument) as e:
                db.delete_channel(channel[0])
                print("Deleted invalid channel with ID " + channel[0])
    await client.close()

# run discord function
client.run(DISCORD_KEY)

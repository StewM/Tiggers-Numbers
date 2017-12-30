import os, sys, discord, asyncio
from os.path import join, dirname
from dotenv import load_dotenv
from datetime import date, datetime
from modules import db

# initialize Discord Client
client = discord.Client()

# load .env file
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# get environment variables
CHANNEL_ID = os.environ.get('CHANNEL_ID')
DISCORD_KEY = os.environ.get('DISCORD_KEY')

# ensure channel table is created
db.create_channel_table()

def checkPermissions(message):
    return message.author.permissions_in(message.channel).administrator

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    # Subscribe to channel
    # On Receive '@mention subscribe'
    if message.content.startswith(client.user.mention + " subscribe"):
        # Check if user has admin permission
        if checkPermissions(message):
            # if so add channel to channels table
            db.add_channel(message.server.id, message.channel.id)
            await client.send_message(message.channel, "Thanks! I'll post my numbers here from now on!")
        else:
            # if not let them know they don't have permission
            await client.send_message(message.channel, "Sorry! Please ask an admin to do this.")
    # Unsubscribe from channel
    # On Receive '@mention unsubscribe'
    elif message.content.startswith(client.user.mention + " unsubscribe"):
        # Check if user has admin permission
        if checkPermissions(message):
            # if so remove channel from channels table
            db.delete_channel(message.channel.id)
            await client.send_message(message.channel, "Alright I won't post my numbers here anymore.")
        else:
            # if not let them know they don't have permission
            await client.send_message(message.channel, "Sorry! Please ask an admin to do this.")
    # See which channels are subscribed on this server
    # On Receive '@mention subscriptions'
    elif message.content.startswith(client.user.mention + " subscriptions"):
        # Get subs for this server
        subs = db.get_subscriptions(message.server.id)
        # If there's subs, list them
        if len(subs) > 0:
            response = "These channels are subscribed: "
            for sub in subs:
                response += client.get_channel(sub[0]).name + ", "
            response = response[:-2]
        else:
            response = "No channels are subscribed."
        await client.send_message(message.channel, response)


client.run(DISCORD_KEY)

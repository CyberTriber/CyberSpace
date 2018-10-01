# coding=utf-8
import discord
import asyncio
from discord.ext.commands import Bot
import os
import time
import datetime

from secrets.discord_secrets import *

# Discord INIT
botName = 'CyberSpace'
command_prefix = '?'

global client
client = Bot(command_prefix=command_prefix, pm_help=True, case_insensitive=True)
client.login(BOT_TOKEN)

while client:
    from functions.game_creator import *
    break

# get actual time
def getTime():
    ts = time.time()
    t = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    return t

# function for formmated text in console (for debugging purposses)
def dprint(data):
    if DEBUG:
        print(getTime()+'\t [DEBUG] - '+data)

# get starting time
start = getTime()

@client.event
async def on_ready():
    print('\033c')
    print(botName+' - version: 0.1.0 Created by CyberCity dev team https://discord.gg/NdrhvcF')
    print(client.user.name+'( '+str(client.user.id)+' )'' is successfuly connected (at '+start+')')
    print('-------------------------------------------------------------------------------')

    await client.change_presence(game=discord.Game(name="CyberSpace", type=1))

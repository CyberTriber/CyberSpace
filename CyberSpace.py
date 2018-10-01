# coding=utf-8
"""
  Discord RPG survival coop game by CyberCity dev team (https://discord.gg/NdrhvcF)
  version: 0.1.0

==============================================================
"""

from secrets.discord_secrets import *		# Import secret info for discord and firebase login
from functions.discord_connect import *		# Import functions to connect discord


def startBot():
	client.run(BOT_TOKEN)

if __name__ == '__main__':
	startBot()

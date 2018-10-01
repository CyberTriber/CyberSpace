from variables.game_creator import *
from . discord_connect import *
import json
import os.path

@client.command(pass_context=True)
async def ping(ctx):
	await ctx.send('pong')

try:
	print(MAX_CHANNELS)
	print(MAX_USERS)
	userList = {}
	print(userList)
except Exception as e:
	print(e)

defRole = {
	'create_instant_invite': False,
	'kick_members': False,
	'ban_members': False,
	'administrator': False,
	'manage_channels': False,
	'manage_guild': False,
	'add_reactions': False,
	'view_audit_log': False,
	'priority_speaker': False,
	'read_messages': False,
	'send_messages': False,
	'send_tts_messages': False,
	'manage_messages': False,
	'embed_links': False,
	'attach_files': False,
	'read_message_history': False,
	'mention_everyone': False,
	'external_emojis': False,
	'connect': False,
	'speak': False,
	'mute_members': False,
	'deafen_members': False,
	'move_members': False,
	'use_voice_activation': False,
	'change_nickname': False,
	'manage_nicknames': False,
	'manage_roles': False,
	'manage_webhooks': False,
	'manage_emojis': False
	}


@client.command(pass_context=True)
async def clear(ctx):
	guild = ctx.message.guild
	roles = guild.roles
	roleList = {}
	chList = {}
	for i in roles:
		roleList[i.name] = i

	for name in roles:
		if name.name.startswith('hra-'):
			await roleList[name.name].delete()
	
	cat = client.get_all_channels()
	for channel in cat:
		if channel.name.startswith('hra-'):
			chList[channel.name]=channel

	for c in chList:
		await chList[c].delete()

	with open(JSON_SERVERS, 'w') as outfile:
				data = {'count': 0}
				json.dump(data, outfile)
	


@client.command(pass_context=True)
async def join(ctx, *args):
	guild = ctx.message.guild
	user = ctx.message.author
	roles = guild.roles
	#print(roles)
	names = []
	roleList = {}
	for i in roles:
		roleList[i.name] = i.id
		#print(i.id)

	for name in roles:
		if name.name.startswith('hra-'):
			names.append(name.name)
	if len(args) == 1:
		if args[0] in names:
			if roleList[args[0]]:
				rid = roleList[args[0]]
				role = await guild.roles(rid)
				await user.add_roles(role)
		else:
			await ctx.send('Taková hra neexistuje')

	elif len(args) == 0:
		if os.path.isfile(JSON_SERVERS):
			currChannel = 1
			with open(JSON_SERVERS, 'r') as outfile:
				srv = json.load(outfile)
				currChannel = int(srv['count'])
		else:
			currChannel = CURR_CH
			with open(JSON_SERVERS, 'w') as outfile:
				data = {'count': currChannel}
				json.dump(data, outfile)

		#await ctx.send(guild)
		if not currChannel:
			currChannel = 0
		game = 'hra-'+str(currChannel)
		try:
			cat = guild.get_channel(GAME_CHANNEL).category
			#print(cat.name)
			
			channel = await guild.create_text_channel(game, category=cat)
			
			with open(JSON_SERVERS, 'w') as outfile:
				data = {'count': currChannel+1}
				json.dump(data, outfile)		
			
			role = await guild.create_role(name=game)
			await user.add_roles(role)
			await ctx.send('User **'+user.name+'** has joined to **'+game+'**')
		except Exception as e:
			print(e)
	else:
		await ctx.send('Chybný počet parametrů příkazu ?join, zadej buď:\n ?join - pro vytvoření nové místnosti\n ?join <název místnosti> - pro připojení k existující hře (?join hra-1)')

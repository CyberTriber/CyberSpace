from variables.game_creator import *
from . discord_connect import *
import json
import os.path


@client.command(pass_context=True)
async def ping(ctx):
    await ctx.send('pong')

@client.event
async def on_guild_channel_create(channel):
	await channel.send(file=discord.File('./static/img/welcome_title.png'))
	await channel.send(welcomeMSG)


@client.command(pass_context=True)
async def players(ctx):
    guild = ctx.message.guild
    roles = guild.roles
    roleList = {}
    chList = {}
    empty = True
    for i in roles:
        roleList[i.name] = i

    for game in roleList:
    	if game.startswith('hra-'):
    	   	await ctx.send('**'+game+'**')
    	   	for players in guild.members:
    	   		for rol in players.roles:
    	   			if rol.name.startswith(game):
    	   				await ctx.send('```      '+players.name+'                                                                              ```')
    	   	await ctx.send('{}'.format('⠀'))
    	   	empty = False
    
    if empty:
    	await ctx.send('Nobody plays at the moment')


@client.command(pass_context=True)
async def clear(ctx):
    guild = ctx.message.guild
    roles = guild.roles
    roleList = {}
    chList = {}
    for i in roles:
        roleList[i.name] = i


    cat = client.get_all_channels()
    for channel in cat:
        if channel.name.startswith('hra-'):
            chList[channel.name] = channel

    
    for name in roles.copy():
        if name.name.startswith('hra-'):
            try:
            	await roleList[name.name].delete()
            	print('deleting '+roleList[name.name])
            	del roleList[name.name]
            	await asyncio.sleep(0.1)
            except:
            	await asyncio.sleep(0.1)


    for c in chList.copy():
        try:
        	await chList[c].delete()
        	print('deleting '+chList[c])
        	del chList[c]
        	await asyncio.sleep(0.1)
        except:
        	await asyncio.sleep(0.1)

    with open(JSON_SERVERS, 'w') as outfile:
        data = {'count': 0}
        json.dump(data, outfile)


@client.command(pass_context=True)
async def join(ctx, *args):
    user = ctx.message.author
    userRole = user.roles
    uRoles = []
    for r in userRole:
        if r.name.startswith('hra-'):
            uRoles.append(r.name)

    matching = [r for r in uRoles if "hra-" in r]
    games = ''
    for g in matching:
        games += g + ' '

    if matching:
        await ctx.send('Už jsi připojen do hry **' + games + '**')
    else:
        guild = ctx.message.guild
        roles = guild.roles
        names = []
        roleList = {}
        for i in roles:
            roleList[i.name] = i
        for name in roles:
            if name.name.startswith('hra-'):
                names.append(name.name)

        if len(args) == 1:
            if args[0] in names:
                if roleList[args[0]]:
                    rid = roleList[args[0]]
                    await user.add_roles(rid)
                    await ctx.send('User **' + user.name + '** has joined to **' + rid.name + '**')
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

            if not currChannel:
                currChannel = 0
            game = 'hra-' + str(currChannel)
            try:
                cat = guild.get_channel(GAME_CHANNEL).category

                channel = await guild.create_text_channel(game, category=cat)

                perms = discord.PermissionOverwrite()
                perms.create_instant_invite = False
                perms.kick_members = False
                perms.ban_members = False
                perms.administrator = False
                perms.manage_channels = False
                perms.manage_guild = False
                perms.add_reactions = False
                perms.view_audit_log = False
                perms.read_messages = True
                perms.send_messages = True
                perms.send_tts_messages = False
                perms.manage_messages = False
                perms.embed_links = False
                perms.attach_files = False
                perms.read_message_history = True
                perms.mention_everyone = False
				# noinspection SpellCheckingInspection
                perms.external_emojis = False
                perms.connect = False
                perms.speak = False
                perms.mute_members = False
                perms.deafen_members = False
                perms.move_members = False
                perms.use_voice_activation = False
                perms.change_nickname = False
                perms.manage_nicknames = False
                perms.manage_roles = False
                perms.manage_webhooks = False
                perms.manage_emojis = False
                await channel.set_permissions(user, overwrite=perms)

                with open(JSON_SERVERS, 'w') as outfile:
                    data = {'count': currChannel + 1}
                    json.dump(data, outfile)

                role = await guild.create_role(name=game)
                await user.add_roles(role)
                await ctx.send('User **' + user.name + '** has joined to **' + game + '**')
            except Exception as e:
                print(e)
        else:
            await ctx.send(
                'Chybný počet parametrů příkazu ?join, zadej buď:\n ?join - pro vytvoření nové místnosti\n ?join <název místnosti> - pro připojení k existující hře (?join hra-1)')

import os
import time
import json
import discord
from discord.ext import commands
from dotenv import load_dotenv
# modules
from controllers import discordo

# load the .env variables
load_dotenv()
# load credentials
token = os.environ["DISCORD"]

# discord configuration
# define the intents
intents = discord.Intents.all()
intents.members = True
# instance the discord app
bot = commands.Bot(command_prefix='-', intents=intents)

# when the bot starts running
@bot.event
async def on_ready():
    print('im alive')

# when a message came
@bot.event
async def on_message(message):

    # if the message was from Lambda
    if message.author == bot.user:
        return

    # if the message was a direct message
    elif not message.guild:
        # send a warning
        await message.author.send("> Lo siento, no acepto mensajes directos")
        # and kill the function
        return

###########################################################################################
#################### Lambda Calls #########################################################
###########################################################################################

############# lambda call in general
    elif message.content[:7] in ['lambda ', 'Lambda ']:
        # in case of error
        try:
            # get the message without 'lambda '
            msg = message.content[7:].strip()
            # call lambda
            answers = discordo.call_lambda(
                msg,
                str(message.author.id),
                str(message.guild.id)
            )
            # send the answers
            for answer in answers['answer']:
                # for images or files
                if answer['type'] == 'file':
                    # open the file, content will be
                    # the file path to open
                    with open(answer['content'], 'rb') as f:
                        # set a discord instance
                        file = discord.File(f)
                        # send the the file
                        await message.channel.send(file=file)
                elif answer['type'] == 'error':
                    # split the answer in pieces
                    pieces = discordo.split_text(answer['content'])
                    # and send them
                    for p in pieces:
                        await message.channel.send('> ' + p)
                # for just text or other things
                else:
                    # split the answer in pieces
                    pieces = discordo.split_text(answer['content'])
                    # and send them
                    for p in pieces:
                        await message.channel.send(p)
        # there was an error
        except Exception as e:
            # save the error code on a str
            error_str = str(e)
            # regist that error on the db
            discordo.db_request('POST', '/errors', {
                "code": error_str,
                "call": message.content[7:].strip(),
                "member": str(message.author.id),
                "server": str(message.guild.id)
            })
            # and send a message
            await message.channel.send(f"> Lo siento, algo salió mal")

############# lambda call for conversation
    elif message.content[:7] in ['lambda,', 'Lambda,']:
        # in case of error
        try:
            # get the message without 'lambda '
            msg = message.content[7:].strip()
            # call lambda
            answers = discordo.call_lambda(
                msg,
                str(message.author.id),
                str(message.guild.id),
                chat=True
            )
            # send the answers
            for answer in answers['answer']:
                # for images or files
                if answer['type'] == 'file':
                    # open the file, content will be
                    # the file path to open
                    with open(answer['content'], 'rb') as f:
                        # set a discord instance
                        file = discord.File(f)
                        # send the the file
                        await message.channel.send(file=file)
                elif answer['type'] == 'error':
                    # split the answer in pieces
                    pieces = discordo.split_text(answer['content'])
                    # and send them
                    for p in pieces:
                        await message.channel.send('> ' + p)
                # for just text or other things
                else:
                    # split the answer in pieces
                    pieces = discordo.split_text(answer['content'])
                    # and send them
                    for p in pieces:
                        await message.channel.send(p)
        # there was an error
        except Exception as e:
            # save the error code on a str
            error_str = str(e)
            # regist that error on the db
            discordo.db_request('POST', '/errors', {
                "code": error_str,
                "call": message.content[7:].strip(),
                "member": str(message.author.id),
                "server": str(message.guild.id)
            })
            # and send a message
            await message.channel.send(f"> Lo siento, algo salió mal")


###########################################################################################
##################### Discord Functions #####################################################
###########################################################################################

############# the manual
    elif message.content in ['Manual', 'manual', 'man']:
        # get the message by pieces
        pieces = discordo.get_public_manual()
        # send the pieces
        for p in pieces:
            await message.channel.send(p)


############# active lockdown room
    # salasegura para [@member1] [@member2] ...
    elif message.content[:11] in ['Salasegura ', 'salasegura ']:
        # get the server info
        server_db = discordo.db_request('GET', '/servers', {
            "id": str(message.guild.id)
        })

        # if the author is not in a voice channel
        if message.author.voice is None:
            await message.channel.send('> Lo siento, primero debes de entrar al canal de voz')

        # there's no white list active, then create one
        elif server_db['lockdown_members'] == []:
            # get the voice channel of the user
            voice_channel = str(message.author.voice.channel)
            # get the message str
            # ids mentions are like <@id>
            members = message.content.split(' ')[2:]
            # extract the ids without symbols
            member_ids = [m[2:-1] for m in members]
            # save the members and the channel in memory
            server_db['lockdown_members'] = member_ids
            server_db['lockdown_channel'] = voice_channel
            # write db
            discordo.db_request('PUT', '/servers', {
                "id": str(message.guild.id),
                "data": server_db
            })
            # send a confirmation
            await message.channel.send(f"ya esta lista la **sala segura** para {' '.join(members)} en **{voice_channel}**")

        # there's a white list active
        else:
            await message.channel.send(f'> Lo siento, no puedo hacer eso, ya hay una **sala segura** activa en {server_db["lockdown_channel"]}')


############# add users to lockdown
    elif message.content[:13] in ['Agregarasala ','agregarasala ']:
        # get the server info
        server_db = discordo.db_request('GET', '/servers', {
            "id": str(message.guild.id)
        })
        # check if the user is in the list
        if str(message.author.id) in server_db['lockdown_members']:
            # get the message str
            # ids mentions are like <@id>
            members = message.content.split(' ')[1:]
            # extract the ids without symbols as a set
            member_ids = set([m[2:-1] for m in members])
            # add the users
            server_db['lockdown_members'] += member_ids
            # write the memory
            # write db
            discordo.db_request('PUT', '/servers', {
                "id": str(message.guild.id),
                "data": server_db
            })
            # and send the message
            await message.channel.send(f"> Listo, miembros agregados a **{server_db['lockdown_channel']}**")
         # if the user is not in the list
        else:
            await message.channel.send(f'> Lo siento, no tienes permiso para hacer eso')


############# remove users from lockdown
    elif message.content[:13] in ['Quitardesala ','quitardesala ']:
        # get the server info
        server_db = discordo.db_request('GET', '/servers', {
            "id": str(message.guild.id)
        })
        # check if the user is in the list
        if str(message.author.id) in server_db['lockdown_members']:
            # get the message str
            # ids mentions are like <@id>
            members = message.content.split(' ')[1:]
            # extract the ids without symbols as a set
            member_ids = set([m[2:-1] for m in members])
            # get the actual members as a set
            actual_ids = set(server_db['lockdown_members'])
            # add the users, as a list
            server_db['lockdown_members'] = list(actual_ids - member_ids)
            # write db
            discordo.db_request('PUT', '/servers', {
                "id": str(message.guild.id),
                "data": server_db
            })
            # and send the message
            await message.channel.send(f"> Listo, miembros eliminados de **{server_db['lockdown_channel']}**")
        # if the user is not in the list
        else:
            await message.channel.send(f'> Lo siento, no tienes permiso para hacer eso')


############# clear lockdown room
    # only lockdown members can clear the list
    elif message.content[:9] in ['Salalibre','salalibre']:
        # get the server info
        server_db = discordo.db_request('GET', '/servers', {
            "id": str(message.guild.id)
        })
        # see if there's not a lockdown active
        if server_db['lockdown_members'] == []:
            await message.channel.send(f"> Lo siento, no hay una **sala segura* activa en **{server_db['lockdown_channel']}**")
        # see if this user is in the members
        elif str(message.author.id) in server_db['lockdown_members']:
            # delete the lockdown list and the channel
            server_db['lockdown_members'] = []
            server_db['lockdown_channel'] = ""
            # write db
            discordo.db_request('PUT', '/servers', {
                "id": str(message.guild.id),
                "data": server_db
            })
            # send a confirmation
            await message.channel.send('> Listo, todos son libres de entrar')
        else:
            await message.channel.send("> Lo siento, no tienes permiso para eso")

###########################################################################################
############## Admin Commands #############################################################
###########################################################################################

    # Admin level: now only for me
    # lambda cli
    # echo function

    elif str(message.author.id) == "717071120175595631":
        
        try:

    ############# lambda cli
            if message.content[:2] == '$ ':
                # this is for the log
                pieces = discordo.lambda_cli(message) # use the lambda_cli controller
                for p in pieces: # send the message or messages
                    await message.channel.send(p)


    ############# echo funcion
            elif message.content[:5] == 'echo ':
                await message.channel.send(f"```{message.content}```")


    ############# upload files
            elif message.content[:7] in ['upload ', 'Upload ']:
                # get the files
                files = message.content.split(' ')[1:]
                # open the files
                for file in files:
                    with open(file, 'rb') as f:
                        # set a discord instance
                        imagen = discord.File(f)
                        # send the image
                        await message.channel.send(file=imagen)
                # app to log
                memory.app_to_log(f'[DISCORD] -> Admin <@{str(message.author.id)}> upload files: {message.content}')

        except:
            memory.app_to_log(f'[ADMIN][ERROR] -> <@{message.author.id}>: {message.content}')
            await message.channel.send(f"> Lo siento, algo salió mal")


###########################################################################################
############## Discord Events #############################################################
###########################################################################################

# kick members that aren't in white list when they join the channel
@bot.event
async def on_voice_state_update(member: discord.Member, before, after):
    # get the server info
    server_db = discordo.db_request('GET', '/servers', {
        "id": str(member.guild.id)
    })

    # Check if member is in a voice channel
    if member.voice is not None and member.voice.channel is not None:
        # get the voice channel name
        voice_channel_name = str(member.voice.channel.name)
        # check if there is an active lockdown and member is in the designated lockdown channel
        if server_db['lockdown_members'] != [] and voice_channel_name == server_db['lockdown_channel']:
            # check if member is not in the whitelist
            if str(member.id) not in server_db['lockdown_members']:
                # disconnect member who is not in the whitelist
                await member.move_to(None)
                

# run the bot
bot.run(token)
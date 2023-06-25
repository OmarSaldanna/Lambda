import discord
import time
from discord.ext import commands
# modules
from controllers import discordo, memory


# load the token
info = memory.get_memory('info')
# requirements to run discord app
token = info['discordo']

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

    if message.author == bot.user:
        return

###########################################################################################
#################### Lambda Calls #########################################################
###########################################################################################

############# lambda calls
    elif message.content[:7] in ['lambda ', 'Lambda ']:
        try:
            # and the user is a member
            if str(message.author.id) in memory.get_memory('info')['members']:
                # the message without 'Lambda '
                msg = message.content[7:]
                # add to log
                memory.app_to_log(f'[DISCORDO] -> called to lambda from <@{str(message.author.id)}>')
                # call lambda
                answers = discordo.call_lambda(msg, str(message.author.id))
                # split the answer in answers
                answers = discordo.split_text('\n'.join(answers))
                # and send them
                for a in answers:
                    await message.channel.send(a)
                    
            # not registered users
            else:
                # add to log
                memory.app_to_log(f'[DISCORDO] -> <@{str(message.author.id)}> not in members called lambda')
                await message.channel.send(f"> Lo siento @<{str(message.author.id)}> no tienes acceso a mi")
                await message.channel.send(f"> Si lo deseas pídele a un admin que te de acceso")
        except:
            memory.app_to_log(f'[LAMBDA][ERROR] -> <@{message.author.id}>: {message.content}')
            await message.channel.send(f"> Lo siento, algo salió mal")

############# lambda calls
    elif message.content[:7] in ['lambda,', 'Lambda,']:
        try:
            # and the user is a member
            if str(message.author.id) in memory.get_memory('info')['members']:
                # the message without 'Lambda '
                msg = message.content[8:]
                # add to log
                memory.app_to_log(f'[DISCORDO] -> conversation from <@{str(message.author.id)}>')
                # call lambda
                answers = discordo.call_lambda(msg, str(message.author.id), on_conversation=True)
                # split the answer in answers
                answers = discordo.split_text('\n'.join(answers))
                # and send them
                for a in answers:
                    await message.channel.send(a)
                    
            # not registered users
            else:
                # add to log
                memory.app_to_log(f'[DISCORDO] -> <@{str(message.author.id)}> not in members called lambda')
                await message.channel.send(f"> Lo siento @<{str(message.author.id)}> no tienes acceso a mi")
                await message.channel.send(f"> Si lo deseas pídele a un admin que te de acceso")
        except:
            memory.app_to_log(f'[LAMBDA][ERROR] -> <@{message.author.id}>: {message.content}')
            await message.channel.send(f"> Lo siento, algo salió mal")

###########################################################################################
##################### Public Commands #####################################################
###########################################################################################

############# the admin manual
    elif message.content in ['Manual', 'manual', 'man']:
        memory.app_to_log(f'[DISCORD] -> Member <@{str(message.author.id)}> called manual')
        # get the message by pieces
        pieces = discordo.get_public_manual()
        # send the pieces
        for p in pieces:
            await message.channel.send(p)


############# active lockdown room
    # salasegura para [@member1] [@member2] ...
    elif message.content[:11] in ['Salasegura ', 'salasegura ']:
        # read the memory
        memory_file = memory.get_memory('memory')

        # if the author is not in a voice channel
        if message.author.voice is None:
            await message.channel.send('> Lo siento, primero debes de entrar al canal de voz')

        # there's no white list active, then create one
        elif memory_file['lockdown_members'] == []:
            # get the voice channel of the user
            voice_channel = str(message.author.voice.channel)
            # get the message str
            msg = message.content
            # ids mentions are like <@id>
            members = msg.split(' ')[2:]
            # extract the ids without symbols
            member_ids = [m[2:-1] for m in members]
            # save the members and the channel in memory
            memory_file['lockdown_members'] = member_ids
            memory_file['lockdown_channel'] = voice_channel
            # write memory
            memory_file.write()
            # send a confirmation
            await message.channel.send(f"ya esta lista la **sala segura** para {' '.join(members)} en **{voice_channel}**")

        # there's a white list active
        else:
            await message.channel.send('> Lo siento, no puedo hacer eso, ya hay una **sala segura** activa')


############# add users to lockdown
    elif message.content[:13] in ['Agregarasala ','agregarasala ']:
        # read the lockdown members
        memory_file = memory.get_memory('memory')
        # check if the user is in the list
        if str(message.author.id) in memory_file['lockdown_members']:
            # get the message str
            msg = message.content
            # ids mentions are like <@id>
            members = msg.split(' ')[1:]
            # extract the ids without symbols as a set
            member_ids = set([m[2:-1] for m in members])
            # add the users
            memory_file['lockdown_members'] += member_ids
            # write the memory
            memory_file.write()
            # and send the message
            await message.channel.send(f"> Listo, miembros agregados a **{memory_file['lockdown_channel']}**")
         # if the user is not in the list
        else:
            await message.channel.send(f'> Lo siento, no tienes permiso para hacer eso')


############# remove users from lockdown
    elif message.content[:13] in ['Quitardesala ','quitardesala ']:
        # read the lockdown members
        memory_file = memory.get_memory('memory')
        # check if the user is in the list
        if str(message.author.id) in memory_file['lockdown_members']:
            # get the message str
            msg = message.content
            # ids mentions are like <@id>
            members = msg.split(' ')[1:]
            # extract the ids without symbols as a set
            member_ids = set([m[2:-1] for m in members])
            # get the actual members as a set
            actual_ids = set(memory_file['lockdown_members'])
            # add the users, as a list
            memory_file['lockdown_members'] = list(actual_ids - member_ids)
            # write the memory
            memory_file.write()
            # and send the message
            await message.channel.send(f"> Listo, miembros eliminados de **{memory_file['lockdown_channel']}**")
        # if the user is not in the list
        else:
            await message.channel.send(f'> Lo siento, no tienes permiso para hacer eso')


############# clear lockdown room
    # only lockdown members can clear the list
    elif message.content[:9] in ['Salalibre','salalibre']:
        # read the lockdown members
        memory_file = memory.get_memory('memory')
        # see if there's not a lockdown active
        if memory_file['lockdown_members'] == []:
            await message.channel.send(f"> Lo siento, no hay una **sala segura* activa en **{memory_file['lockdown_channel']}**")
        # see if this user is in the members
        elif str(message.author.id) in memory_file['lockdown_members']:
            # delete the lockdown list and the channel
            memory_file['lockdown_members'] = []
            memory_file['lockdown_channel'] = ""
            memory_file.write()
            # send a confirmation
            await message.channel.send('> Listo, todos son libres de entrar')
        else:
            await message.channel.send("> Lo siento, no tienes permiso para eso")

###########################################################################################
############## Admin Commands #############################################################
###########################################################################################

    # Admin level
    # lambda cli #
    # add members: add, see, del #
    # lambdrive files: ls, rm, mv #

    elif str(message.author.id) in memory.get_memory('info')['admins']:
        
        try:

    ############# lambda cli
            if message.content[:2] == '$ ':
                # this is for the log
                memory.app_to_log(f'[DISCORD] -> Admin <@{str(message.author.id)}> called lambda-cli -> {message.content[2:]}')
                pieces = discordo.lambda_cli(message) # use the lambda_cli controller
                for p in pieces: # send the message or messages
                    await message.channel.send(p)

    ############# the admin manual
            elif message.content in ['aman', 'Aman']:
                memory.app_to_log(f'[DISCORD] -> Admin <@{str(message.author.id)}> called manual')
                # get the message by pieces
                pieces = discordo.get_admin_manual()
                # send the pieces
                for p in pieces:
                    await message.channel.send(p)

    ############# member admin
            elif message.content[:7] in ['member ','Member ']:

                # add user
                if message.content[7:10] == 'add':
                    # use the controller
                    msg, log = discordo.add_member(message)
                    # make the log
                    memory.app_to_log(log)
                    # and send the message
                    await message.channel.send(msg)

                # see users
                elif message.content[7:] == 'see':
                    # make the log
                    memory.app_to_log(f'[DISCORD] -> Admin <@{str(message.author.id)}> saw members')
                    # and send the result
                    await message.channel.send("**Lista de Miembros**")
                    # show all the vip users
                    for user in memory.get_memory('info')['members']:
                        await message.channel.send(f"> <@{user}>")
                
                # delete user
                elif message.content[7:10] == 'del':
                    # use the controller
                    msg, log = discordo.delete_member(message)
                    # make the log
                    memory.app_to_log(log)
                    # and send the message
                    await message.channel.send(msg)

                # command not understood                
                else:
                    memory.app_to_log(f'[DISCORD] -> Admin <@{str(message.author.id)}> error on members')
                    await message.channel.send("> Escribe bien wey [add|see|del]")
            
    ############# echo funcion
            elif message.content[:5] == 'echo ':
                memory.app_to_log(f'[DISCORD] -> Admin <@{str(message.author.id)}> echoes {message.content[5:]}')
                await message.channel.send(f"```{message.content[5:]}```")


    ############# lambdrive files
            elif message.content[:10] in ['lambdrive ', 'Lambdrive ']:
                # get the command
                command = message.content[10:12]
                # excecute the command
                pieces = discordo.lambdrive_cli(message, command)
                # app to log
                memory.app_to_log(f'[DISCORD] -> Admin <@{str(message.author.id)}> called lambdrive: {message.content[10:]}')
                # send the message
                for p in pieces:
                    await message.channel.send(p)
        except:
            memory.app_to_log(f'[ADMIN][ERROR] -> <@{message.author.id}>: {message.content}')
            await message.channel.send(f"> Lo siento, algo salió mal")

###########################################################################################
############## Discord Events #############################################################
###########################################################################################

# kick members that aren't in white list when they join the channel
@bot.event
async def on_voice_state_update(member: discord.Member, before, after):
    memory_file = memory.get_memory('memory')

    # Check if member is in a voice channel
    if member.voice is not None and member.voice.channel is not None:
        voice_channel_name = str(member.voice.channel.name)
        # Check if there is an active lockdown and member is in the designated lockdown channel
        if memory_file['lockdown_members'] != [] and voice_channel_name == memory_file['lockdown_channel']:
            # Check if member is not in the whitelist
            if str(member.id) not in memory_file['lockdown_members']:
                # Disconnect member who is not in the whitelist
                await member.move_to(None)


# run the bot
bot.run(token)
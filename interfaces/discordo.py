import discord
from discord.ext import commands
# modules
from controllers import discordo, memory


# load the token
info = memory.get_memory('info')
# requirements to run discord app
token = info['discordo']
# members: are allowed to use Lambda
members = info['members']
admins = info['admins']


# discord configuration
# define the intents
intents = discord.Intents.all()
intents.members = True
# instance the discord app
bot = commands.Bot(command_prefix='-', intents=intents)


# when the bot starts running
@bot.event
async def on_ready():
    print('[DISCORDO] -> Lambda -> im alive')


# when a message came
@bot.event
async def on_message(message):

    if message.author == bot.user:
        return

    # if lambda was called
    elif message.content[:7] in ['lambda ', 'Lambda ']:
        # and the user is a member
        if str(message.author.id) in members:
            # the message without 'Lambda '
            msg = message.content[7:]
            # call lambda
            answers = discordo.call_lambda(msg, str(message.author))
            # split the answer in answers
            answers = discordo.split_text('\n'.join(answers))
            # and send them
            for a in answers:
                await message.channel.send(a)

        # not registered users
        else:
            print(str(message.author.id))
            await message.channel.send(f"> Lo siento @{str(message.author)} no tienes acceso a mi")
            await message.channel.send(f"> Si lo deseas pídele a un admin que te de acceso")

    # Admin level
    # lambda cli #
    # add members: add, see, del #
    # lambdrive files: ls, rm, mv #
    elif str(message.author.id) in admins:
############# lambda cli
        if message.content[:2] == '$ ':
            # this is for the log
            memory.app_to_log(f'[DISCORD] -> Admin on lambda-cli -> {message.content[2:]}')
            pieces = discordo.lambda_cli(message) # use the lambda_cli controller
            for p in pieces: # send the message or messages
                await message.channel.send(p)

############# the admin manual
        elif message.content == 'aman':
            memory.app_to_log(f'[DISCORD] -> {message.author} admin manual')
            # get the message by pieces
            pieces = discordo.get_admin_manual()
            # send the pieces
            for p in pieces:
                await message.channel.send(p)

############# member admin
        elif message.content[:7] == 'member ':

            # add user
            if message.content[7:10] == 'add':
                # use the controller
                msg, log = discordo.add_member(message, members, info)
                # make the log
                memory.app_to_log(log)
                # and send the message
                await message.channel.send(msg)

            # see users
            elif message.content[7:] == 'see':
                # make the log
                memory.app_to_log(f'[DISCORD] -> Admin on members -> seen members')
                # and send the result
                await message.channel.send("**Lista de Miembros**")
                # show all the vip users
                for user in members:
                    await message.channel.send(f"> <@{user}>")
            
            # delete user
            elif message.content[7:10] == 'del':
                # use the controller
                msg, log = discordo.delete_member(message, members, info)
                # make the log
                memory.app_to_log(log)
                # and send the message
                await message.channel.send(msg)

            # command not understood                
            else:
                memory.app_to_log(f'[DISCORD] -> Admin on members -> bad command')
                await message.channel.send("> Escribe bien wey [add|see|del]")
        
############# echo funcion
        elif message.content[:5] == 'echo ':
            await message.channel.send(f"```{message.content[5:]}```")


############# lambdrive files
        elif message.content[:10] == 'lambdrive ':
            # get the command
            command = message.content[10:12]
            # excecute the command
            pieces = discordo.lambdrive_cli(message, command)
            # app to log
            memory.app_to_log(f'[DISCORD] -> Admin on lambdrive -> {message.content[10:]}')
            # send the message
            for p in pieces:
                await message.channel.send(p)


############# End of Admin functions
        else:
            memory.app_to_log(f'[DISCORD] -> Admin command -> error')
            await message.channel.send("> Error comando no válido\n> Puedes consultar el manual de admin con _aman_")



# run the bot
bot.run(token)
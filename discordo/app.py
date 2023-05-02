import discord
from modules import controllers
from discord.ext import commands
from modules.memory import *


# load the token
info = get_memory('info')
token = info['DISCORDO']
lambda_ip = info['HOST']['lambda_ip']
lambda_port = info['HOST']['lambda_port']
# the lambda api url
lambda_api = f'http://{lambda_ip}:{lambda_port}/lambda/discordo'

# vip list: close friends that are allowed to use GPT
# admin: me, for lambda backups and lambda-cli
admin = info['ADMIN']
vips = info['VIPS']


# define the intents
intents = discord.Intents.all()
intents.members = True
# instance the discord app
bot = commands.Bot(command_prefix='-', intents=intents)



# when the bot starts running
@bot.event
async def on_ready():
    print('[DISCORDO] -> Lambda -> im alive')
    # app_to_log('[DISCORDO] -> Lambda -> im alive\n')


# when a message came
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Admin level
    # lambda cli #
    # add members #
    # see members #
    # del members #
    if str(message.author) == admin:

        # lambda cli
        if message.content[0] == '$':
            # this is for the log
            app_to_log(f'[DISCORD] -> Admin on lambda-cli -> {message.content[2:]}\n')
            # use the lambda_cli controller
            pieces = controllers.lambda_cli(message)
            # send the message or messages
            for p in pieces:
                await message.channel.send(p)

        # member admin
        if message.content[:7] == 'member ':
            print(message.content[7:])
            # add user
            if message.content[7:10] == 'add':
                # user will be the third argument
                user = message.content.split(' ')[2]
                # if the user is already in vips
                if user in vips:
                    app_to_log(f'[DISCORD] -> Admin on members -> tried to add {user}\n')
                    await message.channel.send(f"> {user} ya está con dios")
                # if the user is not in vips yet
                else:
                    app_to_log(f'[DISCORD] -> Admin on members -> added {user}\n')    
                    # append the user
                    info['VIPS'].append(user)
                    # write changes
                    info.write()
                    # and refresh
                    refresh_users(vips)
                    # send confirmation
                    await message.channel.send(f"> Bienvenido {user} a la buena vida pa")

            # see users
            elif message.content[7:] == 'see':
                app_to_log(f'[DISCORD] -> Admin on members -> seen members\n')
                await message.channel.send("**Lista de VIPs**")
                # show all the vip users
                for user in vips:
                    await message.channel.send(f"> {user}")
            
            # delete user
            elif message.content[7:10] == 'del':
                # user will be the third argument
                user = message.content.split(' ')[2]
                # try to delete the user
                try:
                    # find the idx
                    idx = vips.index(user)
                    # delete it from vips
                    info['VIPS'].pop(idx)
                    # save changes
                    info.write()
                    # and refresh
                    refresh_users(vips)
                    msg = f"> {user} exitosamente bajado del cielo"
                    app_to_log(f'[DISCORD] -> Admin on members -> deleted {user}\n')
                # if there's no user in vips
                except:
                    app_to_log(f'[DISCORD] -> Admin on members -> tried to delete {user}\n')
                    msg = "> No apareció el wey"
                # finally send the mesage
                await message.channel.send(msg)
                

            else:
                app_to_log(f'[DISCORD] -> Admin on members -> bad command\n')
                await message.channel.send("> Escribe bien wey [add|see|del]")



    # VIP Level:
    # status #
    # chat gpt #
    # save stuff 
    # give stuff 
    # fast research 
    # some services
    elif str(message.author) in vips:

        # status
        if message.content in ['tas', 'tas?', 'Tas?']:
            app_to_log(f'[DISCORD] -> {message.author} ping\n')
            # confirmation messgae
            await message.channel.send('> of cors')

        # to see the manual of available functions
        if message.content in ['man', 'manual', 'Manual']:
            app_to_log(f'[DISCORD] -> {message.author} manual\n')
            # return the lambda manual
            await message.channel.send(controllers.get_manual())

        # gpt3 usage
        elif message.content[:7] in ['lambda ', 'Lambda ']:
            app_to_log(f'\n[DISCORD] -> {message.author} on chat gpt -> {message.content}\n')
            # use the chat_gpt controller
            pieces = controllers.chat_gpt(message, lambda_api)
            # add to log the answer
            app_to_log(f"{''.join(pieces)}\n")
            # send the message or messages
            for p in pieces:
                await message.channel.send(p)

        # save stuff
        elif message.content[:9] in ['sostenme ', 'Sostenme ']:
            app_to_log(f'\n[DISCORD] -> {message.author} saved stuff -> {message.content[9:]}\n')
            # save the stuff
            controllers.save_stuff(message)
            # send the confirmation
            await message.channel.send(f"> Listo @{str(message.author)}")

        # save stuff
        elif message.content[:5] in ['dame', 'Dame']:
            app_to_log(f'\n[DISCORD] -> {message.author} read stuff\n')
            # read the stuff
            stuff = controllers.get_stuff(message)
            # send the confirmation
            await message.channel.send(f"> {stuff}")


    # not registered users
    elif message.content[:6] in ['lambda', 'Lambda']:
        await message.channel.send(f"> Lo siento @{str(message.author)} no tienes acceso a mi")
        await message.channel.send(f"> Si lo deseas pídele a @{admin} que te de acceso")

"""  
  # to use an specific command that requires memory or sth
  elif message.content.split(' ')[0] in ['l', 'L']:
    # then consult to lambda
    print(f'[DISCORD] -> Using Command -> {message.content}')
    # send all the mesage without the l or the lambda part
    msg = message.content.split(' ')[1:]
    msg = ' '.join(msg)
    # consult to lambda
    ans = requests.get(lambda_api + '/commands', headers={'msg':msg}).json()
    print(ans['answer'])
    await message.channel.send(ans['answer'])
"""

# run the bot
bot.run(token)

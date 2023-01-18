import os
os.system('clear') # clear screen


# access to lambda memory
from memory.memory import Memory
# lambda interfaces to communications
# Discord, Email, Whatsapp and API
from interfaces import Discord
# Lambda old module of AI
from ai.brain import AI
# other things
from dotenv import load_dotenv

load_dotenv() # load the env variables

# read tokens
discord_token = os.environ.get("DISCORDO")
openai_token = os.environ.get("OPENAI")


def main():
  # 1 - deploy memory
  memory = Memory('./src/memory/data/memory.txt')
  vocab = Memory('./src/memory/data/vocab.txt')

  # 2 - deploy ia
  ai = AI(openai_token)

  # 3.1 deploy controllers

  # 3.2 - deploy comunication interfaces
  Discord.deploy_discord(discord_token) # goes at the end


main()
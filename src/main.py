# access to lambda memory
from memory.memory import Memory
# lambda interfaces to communications
# Discord, Email, Whatsapp and API
from interfaces import Discord
# Lambda old module of IA
from model.brain import Use
# other things
from dotenv import load_dotenv
import os

path = './src/'
load_dotenv()

# read tokens
discord_token = os.environ.get("DISCORDO")
openai_token = os.environ.get("OPENAI")

def main():
  # 1 - deploy memory
  memory = Memory(path + 'data/data/memory.txt')
  vocab = Memory(path + 'data/data/vocab.txt')

  # 2 - deploy ia modules
  use = Use() # this one is to correct 

  # 3 - deploy comunication interfaces
  Discord.deploy_discord(discord_token)


main()
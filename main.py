import discord
from discord.ext import commands
import json
import sys

bot = discord.Client()

def update_file():
  with open('config.json', 'w') as fileOut:
    json.dump(config, fileOut, indent=2, sort_keys=True)

def import_config():
  global config
  try:
    print("Importing configuration...")
    with open('config.json', 'r') as file_in:
      config = json.load(file_in)
  except FileNotFoundError:
    print("Config file not found, creating...")
    with open('config.json', 'w+') as file_out:
      config_temp = {"token": "", "admin_ids": [""], "servers": [{}]}
      json.dump(config_temp, file_out, indent=2, sort_keys=True)
    print("Please put your bot's token in the 'token' key in config.json")
    sys.exit()

if __name__ == '__main__':
  import_config()
  try:
    bot.run(config['token'])
  except discord.errors.LoginFailure as e:
    print(str(e))
    sys.exit()
  except Exception as e:
    print(type(e).__name__ + ": " + str(e))

import json
import os
import sys

import discord
from discord.ext import commands

from utils import prettyoutput as po

bot = commands.Bot(command_prefix="a|")


async def logging(log_type="none", contents=""):
  global config
  try:
    if not config['log_channel_id'] == "":
      await bot.send_message(bot.get_channel(config['log_channel_id']), contents)
  except NameError:
    pass
  if log_type == "info":
    print(po.info(string=contents, prn_out=False))
  elif log_type == "error":
    print(po.error(string=contents, prn_out=False))
  elif log_type == "warn":
    print(po.warn(string=contents, prn_out=False))
  elif log_type == "success":
    print(po.success(string=contents, prn_out=False))
  elif log_type == "none":
    print(contents)


def update_file():
  with open('config.json', 'w') as fileOut:
    json.dump(config, fileOut, indent=2, sort_keys=True)


def import_config():
  try:
    logging("info", "Importing configuration...")
    with open('config.json', 'r') as file_in:
      return json.load(file_in)
  except FileNotFoundError:
    logging("error", "Config file not found, creating...")
    with open('config.json', 'w+') as file_out:
      config_temp = {"token": "", "admin_ids": [""], "servers": [{}]}
      json.dump(config_temp, file_out, indent=2, sort_keys=True)
    logging("error", "Please put your bot's token in the 'token' key in config.json")
    sys.exit()


def add_cogs():
  logging("info", "Getting all extensions in the cogs folder...")
  startup_extensions = []
  for cog in os.popen('ls cogs/').read().split('\n'):
    if not cog == "":
      startup_extensions.append("cogs." + cog.split('.')[0])
  return startup_extensions


@bot.event
async def on_ready():
  await logging("success", 'Successfully logged into discord')
  await logging("info", "{}#{} ({})".format(bot.user.name, bot.user.discriminator, bot.user.id))
  if not config['log_channel_id'] == "":
    try:
      await logging("info", 'Console messages will be send to channel #{} ({}) in {} ({})'.format(bot.get_channel(config['log_channel_id']).name, bot.get_channel(config['log_channel_id']).id, bot.get_channel(config['log_channel_id']).server.name, bot.get_channel(config['log_channel_id']).server.id))
    except AttributeError:
      await logging("error", 'The bot could not access the log channel')

  await bot.change_presence(game=discord.Game(name='Alpha Bot indev'))

  for extension in add_cogs():
    await logging("info", "Loading {}...".format(extension))
    try:
      bot.load_extension(extension)
    except Exception as e:
      exc = '{}: {}'.format(type(e).__name__, e)
      await logging("error", 'Failed to load extension {}\n{}'.format(extension, exc))
  await logging("success", "All extensions loaded successfully")


@bot.event
async def on_message(message):
  await bot.process_commands(message)

# defined here so it can't be accidentally unloaded


@bot.command(name="reload", hidden=True, pass_context=True)
async def reload_module(ctx, module):
  global config
  if ctx.message.author.id in config['admin_ids']:
    bot.unload_extension(module)
    bot.load_extension(module)
    await bot.say("done")

if __name__ == '__main__':
  config = import_config()
  if config['log_channel_id'] == "":
    logging(
        "info", "No log channel set, all status messages will be printed to the console.")
  try:
    logging("info", "Logging into discord")
    bot.run(config['token'])
  except discord.errors.LoginFailure as e:
    logging("error", str(e))
    sys.exit()
  except Exception as e:
    logging("error", type(e).__name__ + ": " + str(e))

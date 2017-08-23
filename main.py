import asyncio
import json
import math
import os
import sys
import time
import traceback
from datetime import datetime

import discord
import pathvalidate
import requests
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont

from utils import prettyoutput as po

start_time = time.time()


def get_prefix(bot, message):
  try:
    with open('config.json') as file_in:
      local_config = json.load(file_in)
  except FileNotFoundError:
    return ""
  if message.content.startswith(f'{message.server.me.mention} '):
    return f'{message.server.me.mention} '
  elif message.content.startswith(f'{bot.user.mention} '):
    return f'{bot.user.mention} '.format(bot)
  if not message.server:
    return local_config['prefix']
  if not message.mentions == []:
    for mention in message.mentions:
      if mention == bot.user:
        return bot.user.mention
  for server in local_config['servers']:
    if server['id'] == message.server.id:
      return server['prefix']


try:
  description = "Alpha, the everything in one discord bot"
  bot = commands.Bot(command_prefix=get_prefix, description=description)
  with open('CHANGELOG.md') as file_in:
    bot.version = file_in.read().split('[')[4].split(']')[0]
  bot.voice_reload_cache = None
except FileNotFoundError:
  pass


async def startup():
  bot.config = await import_config()
  if bot.config['log_channel_id'] == "":
    await logging(
        "info", "No log channel set, all status messages will be printed to the console.")
  await logging("info", "Logging into discord...")


async def logging(log_type="none", contents="", no_print=False):
  try:
    if not bot.config['log_channel_id'] == "" and bot.is_logged_in:
      log_embed = discord.Embed(description=contents, timestamp=datetime.now())
      await bot.send_message(bot.get_channel(bot.config['log_channel_id']), embed=log_embed)
  except:
    pass
  if no_print:
    return
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
    json.dump(bot.config, fileOut, indent=2, sort_keys=True)


async def import_config():
  try:
    await logging("info", "Importing configuration...")
    with open('config.json', 'r') as file_in:
      return json.load(file_in)
  except FileNotFoundError:
    await logging("error", "Config file not found, creating...")
    with open('config.json', 'w+') as file_out:
      config_temp = {"token": "", "admin_ids": [""], "servers": [
      ], "log_channel_id": "", "prefix": "", "dbl-token": ""}
      json.dump(config_temp, file_out, indent=2, sort_keys=True)
    await logging("error", "Please put your bot's information in config.json")
    sys.exit()


async def add_cogs():
  await logging("info", "Getting all extensions in the cogs folder...")
  startup_extensions = []
  for cog in os.listdir('cogs'):
    if not cog == "" and not cog.startswith('.') and not cog.startswith('_'):
      startup_extensions.append("cogs." + cog.split('.')[0])
  return startup_extensions


@bot.event
async def on_ready():
  global start_time
  if not bot.config['log_channel_id'] == "":
    try:
      await logging("info", 'Console messages will be send to channel #{} \n\t\t({}) in {} ({})'.format(bot.get_channel(bot.config['log_channel_id']).name, bot.get_channel(bot.config['log_channel_id']).id, bot.get_channel(bot.config['log_channel_id']).server.name, bot.get_channel(bot.config['log_channel_id']).server.id))
    except AttributeError:
      bot.config['log_channel_id'] = ""
      await logging("error", "The bot cannot access the log channel")
  await logging("success", 'Successfully logged into discord as\n\t\t{}#{} ({})'.format(bot.user.name, bot.user.discriminator, bot.user.id))

  await bot.change_presence(game=discord.Game(name='%help for help'))

  for extension in await add_cogs():
    await logging("info", "Loading {}...".format(extension))
    try:
      bot.load_extension(extension)
    except Exception as e:
      exc = '{}: {}'.format(type(e).__name__, e)
      await logging("error", 'Failed to load extension {}\n{}'.format(extension, exc))
  await logging("success", "All extensions loaded")

  for server in bot.servers:
    if not server.id in [server['id'] for server in bot.config['servers']]:
      bot.config['servers'].append({"id": server.id, "enabled_modules": [
                                   "Fun", "Misc", "Nsfw"], "prefix": bot.config['prefix'], "mod_ids": [], "welcome_channel": server.id})
      update_file()

  for server in bot.config['servers']:
    if not server['id'] in [server.id for server in bot.servers]:
      bot.config['servers'].remove(server)
      update_file()

  end_time = time.time() - start_time
  await logging("info", "Started in {} seconds ({} ms)".format(math.floor(end_time), math.floor(end_time * 1000)))


@bot.event
async def on_message(message):
  await bot.process_commands(message)


@bot.event
async def on_server_join(server):
  bot.config['servers'].append({"id": server.id, "enabled_modules": ["Fun", "Misc", "Nsfw"],
                                "prefix": bot.config['prefix'], "mod_ids": [], "welcome_channel": server.id})
  update_file()
  slash_n = "\n"
  await logging("info", f"**I joined a server!**{slash_n}Name: **{server.name}**{slash_n}ID: {server.id}{slash_n}Members: {server.member_count}{slash_n}Bot Servers: {len(bot.servers)}", no_print=True)


@bot.event
async def on_server_leave(server):
  for this_server in bot.config['servers']:
    if this_server['id'] == server.id:
      bot.config['servers'].remove(this_server)
  update_file()
  slash_n = "\n"
  await logging("info", f"**I left a server**{slash_n}Name: **{server.name}**{slash_n}ID: {server.id}{slash_n}Members: {server.member_count}{slash_n}Bot Servers: {len(bot.servers)}", no_print=True)


@bot.event
async def on_member_join(member):
  if not "Welcome" in [server['enabled_modules'] for server in bot.config['servers'] if server['id'] == member.server.id][0]:
    return
  template = Image.open('extras/template.png')
  draw = ImageDraw.Draw(template)
  user = member.name
  server = member.server.name
  img_fraction = 0.50
  fontsize = 16
  member_name = pathvalidate.sanitize_filename(
      member.name).replace('(', '').replace(')', '').replace(' ', '')
  server_name = pathvalidate.sanitize_filename(
      member.server.name).replace('(', '').replace(')', '').replace(' ', '')
  if member.avatar_url == "":
    member_avatar = requests.get(member.default_avatar_url)
  else:
    member_avatar = requests.get(member.avatar_url)
  with open('extras/{}.png'.format(member_name), 'wb') as f:
    for chunk in member_avatar.iter_content(chunk_size=1024):
      if chunk:
        f.write(chunk)
  member_avatar = Image.open('extras/{}.png'.format(member_name))
  member_avatar = member_avatar.resize((182, 182), Image.ANTIALIAS)
  template.paste(member_avatar, (34, 71))
  guild_icon = requests.get(member.server.icon_url)
  with open('extras/{}.png'.format(server_name), 'wb') as f:
    for chunk in guild_icon.iter_content(chunk_size=1024):
      if chunk:
        f.write(chunk)
  guild_icon = Image.open('extras/{}.png'.format(server_name))
  guild_icon = guild_icon.resize((64, 64), Image.ANTIALIAS)
  template.paste(guild_icon, (660, 300))
  font = ImageFont.truetype("extras/segoeui.ttf", fontsize)
  while font.getsize(user)[0] < img_fraction * template.size[0]:
    fontsize += 1
    font = ImageFont.truetype("extras/segoeui.ttf", fontsize)
  fontsize -= 1
  font = ImageFont.truetype("extras/segoeui.ttf", fontsize)
  if len(user) < 6:
    font = ImageFont.truetype("extras/segoeui.ttf", 58)
  draw.text((125, 290), user, (0, 0, 0), font=font)

  fontsize = 16
  img_fraction = 0.25
  font = ImageFont.truetype("extras/segoeui.ttf", fontsize)
  while font.getsize(server)[0] < img_fraction * template.size[0]:
    fontsize += 1
    font = ImageFont.truetype("extras/segoeui.ttf", fontsize)
  fontsize -= 1
  font = ImageFont.truetype("extras/segoeui.ttf", fontsize)
  if len(server) < 6:
    font = ImageFont.truetype("extras/segoeui.ttf", 32)
  draw.text((540, 255), server, (0, 0, 0), font=font)

  template.save('extras/finished.png')
  await bot.send_file(member.server.get_channel([server['welcome_channel'] for server in bot.config['servers'] if server['id'] == member.server.id][0]), 'extras/finished.png')
  os.remove('extras/finished.png')
  os.remove('extras/{}.png'.format(member_name))
  os.remove('extras/{}.png'.format(server_name))


@bot.command(name="reload", hidden=True, pass_context=True)
async def reload_module(ctx, module):
  if not ctx.message.author.id in bot.config['admin_ids']:
    return
  bot.unload_extension(module)
  try:
    bot.load_extension(module)
  except Exception as e:
    await bot.say(type(e).__name__ + ": " + str(e))
    await logging("error", type(e).__name__ + ": " + str(e))
  else:
    await bot.say('Module {} reloaded!'.format(module))
    await logging("info", "Module {} reloaded".format(module))


@bot.command("unload", hidden=True, pass_context=True)
async def unload_module(ctx, module):
  if not ctx.message.author.id in bot.config['admin_ids']:
    return
  bot.unload_extension(module)
  await bot.say('Module {} unloaded!'.format(module))
  await logging("info", "Module {} unloaded".format(module))


@bot.event
async def on_command_error(exception, context):
  if type(exception) == discord.ext.commands.errors.CommandNotFound:
    return
  message = context.message
  tb = ''.join(traceback.format_exception(
      type(exception), exception, exception.__traceback__))
  reply = "COMMAND **{}** IN **{}** ({})".format(
      message.content, message.server.name, message.server.id)
  reply += "\n```py\n{}```".format(tb[len(reply) - 1988:])
  await logging("error", reply)

if __name__ == '__main__':
  loop = asyncio.get_event_loop()
  loop.run_until_complete(asyncio.gather(startup()))
  try:
    bot.run(bot.config['token'])
  except discord.errors.LoginFailure as e:
    print(str(e))
    sys.exit()
  except Exception as e:
    print(type(e).__name__ + ": " + str(e))

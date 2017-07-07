"""
for changing server-wide bot settings
"""
import discord
from discord.ext import commands
import json

class Settings:
  def __init__(self, bot_):
    self.bot = bot_
    with open('config.json') as file_in:
      self.config = json.load(file_in)

  def update_file():
    with open('config.json', 'w') as fileOut:
      json.dump(self.config, fileOut, indent=2, sort_keys=True)

  def is_mod(self, context):
    if context.message.channel.permissions_for(context.message.author).administrator:
      return True
    for server in self.config['servers']:
      if server['id'] == context.message.server.id:
        if context.message.author.id in server['mod_ids']:
          return True
        break
    return False

  @commands.group(name="module")
  async def module_changes(self):
    pass

  @module.command(name="enable", pass_context=True, check=self.is_mod)
  async def enable_module(self, ctx, *module):
  """
  Enables a module in the current server
  """
    for server in self.config['servers']:
      if server['id'] == ctx.message.server.id:
        if not module in server['enabled_modules']:
          server['enabled_modules'].append(module)
          await self.bot.say('{} has been enabled'.format(module))
        else:
          await self.bot.say('{} is already enabled'.format(module))
        break

  @module.command(name="disable", pass_context=True, check=self.is_mod)
  async def disable_module(self, ctx, *module):
  """
  Disables a module in the current server
  """
    for server in self.config['servers']:
      if server['id'] == ctx.message.server.id:
        if module in server['enabled_modules']:
          server['enabled_modules'].remove(module)
          await self.bot.say('{} has been disabled'.format(module))
        else:
          await self.bot.say('{} is already disabled'.format(module))
        break

  @commands.command(name="prefix", pass_context=True, check=self.is_mod)
  async def change_prefix(self, ctx, *new_prefix):
  """
  Changes the bot prefix for the current server
  """
    for server in self.config['servers']:
      if server['id'] == ctx.message.server.id:
        server['prefix'] = new_prefix
        break
    await self.bot.say('Prefix set to {}'.format(new_prefix))

  @commands.group(name="mod")
  async def mod_changes():
    pass

  @mod.command(name="add", pass_context=True, check=self.is_mod)
  async def add_mod(self, ctx, *mod):
    """
    Adds a user as a server mod (from mention or id)
    """
    if not ctx.messsage.mentions = []:
      mod = ctx.messsage.mentions[0].id
    for server in self.config['servers']:
      if server['id'] == ctx.message.server.id:
        if not mod in server['mod_ids']:
          server['mod_ids'].append(mod)
          await self.bot.say('{} has been added as a moderator'.format(mod))
        else:
          await self.bot.say('{} is already a moderator'.format(mod))
        break

  @mod.command(name="remove", pass_context=True, check=self.is_mod)
  async def add_mod(self, ctx, *mod):
    """
    Removes a user as a server mod (from mention or id)
    """
    if not ctx.messsage.mentions = []:
      mod = ctx.messsage.mentions[0].id
    for server in self.config['servers']:
      if server['id'] == ctx.message.server.id:
        if mod in server['mod_ids']:
          server['mod_ids'].remove(mod)
          await self.bot.say('{} has been removed as a moderator'.format(mod))
        else:
          await self.bot.say('{} is not a moderator'.format(mod))
        break

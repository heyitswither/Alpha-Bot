"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

import json

import discord
from discord.ext import commands

from utils.chat_formatting import pagify


class Help:

  def __init__(self, bot):
    self.bot = bot
    self.helplist = "**Links**:\n\u27ab Server: [https://discord.io/wither](https://discord.io/wither)\n\u27ab Bot: [https://bot.discord.io/alpha](https://bot.discord.io/alpha)\n**Commands**:\n"
    bot.remove_command("help")

  def get_prefix(self, bot, message):
    try:
      with open('config.json') as file_in:
        local_config = json.load(file_in)
    except FileNotFoundError:
      return ""
    if message.content.startswith('{} '.format(message.server.me.mention)):
      return '{0.me.mention} '.format(message.server)
    elif message.content.startswith('{} '.format(bot.user.mention)):
      return '{0.user.mention} '.format(bot)
    if not message.server:
      return local_config['prefix']
    if not message.mentions == []:
      for mention in message.mentions:
        if mention == bot.user:
          return bot.user.mention
    for server in local_config['servers']:
      if server['id'] == message.server.id:
        return server['prefix']

  def make_help_list(self, bot, ctx):
    listed = []
    for key, value in self.bot.commands.items():
      command = value
      if command.hidden:
        continue
      if command.name in listed:
        continue
      self.helplist += f"{self.get_prefix(bot, ctx.message)}**__{command.name}__** - {command.short_doc}\n"
      listed.append(command.name)

  @commands.command(name="help", pass_context=True)
  async def _help(self, ctx, command=None):
    """Shows help menu."""
    user = ctx.message.author
    try:
      if not command:
        if self.helplist == "**Links**:\n\u27ab Server: [https://discord.io/wither](https://discord.io/wither)\n\u27ab Bot: [https://bot.discord.io/alpha](https://bot.discord.io/alpha)\n**Commands**:\n":
          self.make_help_list(self.bot, ctx)

        for page in pagify(self.helplist, ['\n']):
          embed = discord.Embed(description=page, color=discord.Color.blue())
          embed.set_author(icon_url=self.bot.user.avatar_url, name=self.bot.user.name + " Help!")
          embed.set_footer(text='End Of Help Page', icon_url=self.bot.user.avatar_url)
          await self.bot.say(embed=embed)
      else:
        msg = "**Command Help:**"
        em = discord.Embed(description=msg, color=discord.Color.purple())
        em.set_author(icon_url=self.bot.user.avatar_url, name=self.bot.user.name)
        try:
          comg = "```\n"
          comg += command
          comg += "\n```"
          info = self.bot.commands[command].help
          em.add_field(name=comg, value=info, inline=False)
          user = ctx.message.author
          await self.bot.say( embed=em)
        except Exception as e:
          print(e)
          await self.bot.say("\U0000274c Couldn't find command! Try again.")
    except Exception as e:
      await self.bot.say(type(e).__name__ + " :" + str(e))
      await self.bot.say("\U0000274c **error** You must give this bot embed permissions")


def setup(bot):
    bot.add_cog(Help(bot))

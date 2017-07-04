"""
bot info, server info, user info, any other info; all goes here
"""

from platform import python_version

import discord
from discord.ext import commands


class Info:
  def __init__(self, bot_):
    self.bot = bot_

  @commands.command(name="info")
  async def bot_info(self):
    info_embed = discord.Embed()
    info_embed.set_author(name="Alpha Bot", url="https://discord.io/wither", icon_url=self.bot.user.avatar_url)
    info_embed.set_thumbnail(url=self.bot.user.avatar_url + "?size=128x128")
    info_embed.add_field(
        name="Description", value="The everything in one discord bot.", inline=False)
    info_embed.add_field(
        name="GitHub", value="https://github.com/heyitswither/Alpha-Bot", inline=False)
    info_embed.add_field(
        name="Python", value="[{}](https://www.python.org/)".format(python_version(), inline=False))
    info_embed.add_field(
        name="Discord.py", value="[{}](https://github.com/Rapptz/discord.py)".format(discord.__version__), inline=True)
    info_embed.add_field(name="Bot Guilds", value=len(
        self.bot.servers), inline=True)
    members = 0
    for member in self.bot.get_all_members():
      members += 1
    info_embed.add_field(name="Bot Users", value=members, inline=True)
    info_embed.add_field(name="Bot Version", value="0.1 indev", inline=True)
    info_embed.add_field(name="Bot Author", value="heyitswither#4340", inline=True)
    await self.bot.say(embed=info_embed)

  @commands.command(name="serverinfo", pass_context=True)
  async def server_info(self, ctx, server_id="ctx"):
    if server_id == "ctx":
      server_id = ctx.message.server.id
    try:
      int(server_id)
    except ValueError:
      pass
    else:
      if not self.bot.get_server(server_id) is None:
        await self.bot.say("Soom:tm: {}".format(server_id))
      else:
        await self.bot.say("I'm not in that server!")

  @commands.command(name="userinfo", pass_context=True)
  async def user_info(self, ctx, user="ctx"):
    if user == "ctx":
      user = ctx.message.author
    else:
      for mention in ctx.message.mentions:
        user = mention
    await self.bot.say("Soom:tm: {}".format(user.mention))


def setup(bot):
  bot.add_cog(Info(bot))

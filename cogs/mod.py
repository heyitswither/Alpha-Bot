"""
server moderation tools
"""

import json

import discord
from discord.ext import commands


class Mod:
  def __init__(self, bot_):
    self.bot = bot_
    with open('config.json') as file_in:
      self.config = json.load(file_in)

  def is_mod(self, context):
    if context.message.channel.permissions_for(context.message.author).administrator or context.message.author.id in self.config['admin_ids']:
      return True
    for server in self.config['servers']:
      if server['id'] == context.message.server.id:
        if context.message.author.id in server['mod_ids']:
          return True
        break
    return False

  @commands.command(name="announce", pass_context=True)
  async def announce(self, ctx, *announcement):
    """
    sends an announcement to the current server
    """
    if not self.is_mod(ctx): return
    announcement = ' '.join(announcement)
    embed = discord.Embed(title="NEW ANNOUNCEMENT", description=announcement)
    embed.set_author(name=ctx.message.author.name + "#" + ctx.message.author.discriminator, icon_url=ctx.message.author.avatar_url)
    try:
      if "announcements" in [channel.name for channel in ctx.message.server.channels]:
        for channel in ctx.message.server.channels:
          if channel.name == "announcements":
            await self.bot.send_message(channel, embed=embed)
      else:
        await self.bot.send_message(ctx.message.server, embed=embed)
    except discord.errors.Forbidden:
      await self.bot.say(":warning: I don't have permissions to send messages in that channel.")

  @commands.command(name="kick", pass_context=True)
  async def kick(self, ctx, user: discord.User):
    """
    kick a user
    """
    if not self.is_mod(ctx): return
    try:
      await self.bot.kick(user)
    except discord.errors.Forbidden:
      await self.bot.say("I require the `Kick Members` permission")
    else:
      await self.bot.say("{} has been kicked".format(user.mention))

  @commands.command(name="ban", pass_context=True)
  async def ban(self, ctx, user: discord.User):
    """
    bans a user
    """
    if not self.is_mod(ctx): return
    try:
      await self.bot.ban(user)
    except discord.errors.Forbidden:
      await self.bot.say("I require the `Ban Members` permission")
    else:
      await self.bot.say("{} has been banned".format(user.mention))

  @commands.command(name="hackban", pass_context=True)
  async def hackban(self, ctx, user: str = None):
    if not self.is_mod(ctx): return
    if not user:
      return await self.bot.say("You must provide a user id to ban")
    try:
      await self.bot.http.ban(user, ctx.message.server.id)
    except discord.errors.NotFound:
      return await self.bot.reply("I could not find the user you are trying to ban")
    except discord.errors.Forbidden:
      return await self.bot.reply("I require the `Ban Members` permission")
    await self.bot.reply("The user has been banned")

def setup(bot):
  bot.add_cog(Mod(bot))

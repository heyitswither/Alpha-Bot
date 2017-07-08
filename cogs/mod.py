"""
server moderation tools
"""

import discord
from discord.ext import commands

class Mod:
  def __init__(self, bot_):
    self.bot = bot_

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
    if "announcements" in [channel.name for channels in ctx.message.server.channels]:
      for channel in ctx.message.server.channels:
        if channel.name == "announcements":
          await self.bot.send_message(channel, embed=embed)
    else:
      await self.bot.send_message(ctx.message.server, embed=embed)

def setup(bot):
  bot.add_cog(Mog(bot))

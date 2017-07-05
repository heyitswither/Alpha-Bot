import discord
from discord.ext import commands

class Misc:
  def __init__(self, bot_):
    self.bot = bot_

  def clean_check(self, message):
    if message.content.startswith(self.bot.command_prefix) or message.author == self.bot.user:
      return True
    return False

  @commands.command(name="clean", pass_context=True)
  async def clean_spam(self, ctx, count: int = -1):
    if count == -1:
      await self.bot.say("You need to include a number of messages to delete.")
    elif count > 200:
      await self.bot.say("That's too many messages.")
    else:
      try:
        await self.bot.delete_message(ctx.message)
        await self.bot.purge_from(ctx.message.channel, limit=count, check=self.clean_check)
      except discord.errors.Forbidden:
        await self.bot.say("I require the `Manage Messages` permission to perform this action.")

def setup(bot):
  bot.add_cog(Misc(bot))

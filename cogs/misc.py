import discord
from discord.ext import commands
import time
import json
import requests

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

  @commands.command(name="ping")
  async def ping_command(self):
    pingtime = time.time()
    pingms = await self.bot.say("Pinging...")
    ping = (time.time() - pingtime) * 1000
    await self.bot.edit_message(pingms, "Ping ==> _**%.01f ms**_ :thumbsup:" % ping)

  @commands.command(name="google", pass_context=True)
  async def google(self, ctx, *query):
    r = requests.get('https://www.googleapis.com/customsearch/v1?key=AIzaSyDu7_tL50kfEcegjXnYqfBxXrKqBrknkkY&cx=013036536707430787589:_pqjad5hr1a&q={}&alt=json'.format(' '.join(query)))
    r = json.loads(r.text)
    embed = discord.Embed(title=r['items'][0]['title'], description="{}\n\n[View More Results](https://www.google.com/search?q={})".format(r['items'][0]['snippet'], ' '.join(query).replace(' ', '+')), url=r['items'][0]['link'])
    embed.set_author(name="{} - Google Search".format(' '.join(query)), icon_url='https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/1000px-Google_%22G%22_Logo.svg.png')
    embed.set_image(url=r['items'][0]['pagemap']['cse_thumbnail'][0]['src'])
    embed.set_footer(text="About {} results ({} seconds)".format(r['searchInformation']['formattedTotalResults'], r['searchInformation']['formattedSearchTime']))
    await self.bot.say(embed=embed)

def setup(bot):
  bot.add_cog(Misc(bot))

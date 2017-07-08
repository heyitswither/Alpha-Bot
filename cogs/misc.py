"""
miscellaneous commands that may or may not be useful
"""
import discord
from discord.ext import commands
import time
import json
import requests

class Misc:
  def __init__(self, bot_):
    self.bot = bot_
    with open('config.json') as file_in:
      self.config = json.load(file_in)

  def update_config(self):
    with open('config.json', 'r') as file_in:
      self.config = json.load(file_in)

  def clean_check(self, context):
    for server in config['servers']:
      if server['id'] == context.message.server.id:
        server_prefix = server['prefix']
        break
    if context.message.content.startswith(self.bot.command_prefix) or content.message.content.startswith(server_prefix) or context.message.author == self.bot.user:
      return True
    return False

  def module_check(self, context):
    self.update_config()
    for server in self.config['servers']:
      if server['id'] == context.message.server.id:
        if "Misc" in server['enabled_modules']:
          if context.command.name == "clean":
            return clean_check(self, context)
          else:
            return True
        break
    return False

  @commands.command(name="clean", pass_context=True)
  async def clean_spam(self, ctx, count: int = -1):
    if not self.module_check(ctx): return
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

  @commands.command(name="ping", pass_context=True)
  async def ping_command(self, ctx):
    if not self.module_check(ctx): return
    pingtime = time.time()
    pingms = await self.bot.say("Pinging...")
    ping = (time.time() - pingtime) * 1000
    await self.bot.edit_message(pingms, "Ping ==> _**%.01f ms**_ :thumbsup:" % ping)

  @commands.command(name="google", pass_context=True)
  async def google(self, ctx, *query):
    if not self.module_check(ctx): return
    r = requests.get('https://www.googleapis.com/customsearch/v1?key=AIzaSyDu7_tL50kfEcegjXnYqfBxXrKqBrknkkY&cx=013036536707430787589:_pqjad5hr1a&q={}&alt=json'.format(' '.join(query)))
    r = json.loads(r.text)
    try:
      embed = discord.Embed(title=r['items'][0]['title'], description="{}\n\n[View More Results](https://www.google.com/search?q={})".format(r['items'][0]['snippet'], ' '.join(query).replace(' ', '+')), url=r['items'][0]['link'])
    except KeyError:
      embed = discord.Embed(title=":warning: No results found")
    try:
      embed.set_image(url=r['items'][0]['pagemap']['cse_thumbnail'][0]['src'])
    except KeyError:
      pass
    embed.set_author(name="{} - Google Search".format(' '.join(query)), icon_url='https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/1000px-Google_%22G%22_Logo.svg.png')

    embed.set_footer(text="About {} results ({} seconds)".format(r['searchInformation']['formattedTotalResults'], r['searchInformation']['formattedSearchTime']))
    await self.bot.say(embed=embed)

  @commands.command(name="suggest", pass_context=True)
  async def suggest(self, ctx, *suggestion):
    """
    suggest a new feature for the bot
    """
    suggestion = ' '.join(suggestion)
    embed = discord.Embed(title="New Suggestion", description=suggestion)
    embed.set_author(name=ctx.message.author.name + "#" + ctx.message.author.discriminator + "(" + ctx.message.author.id + ")")
    await self.bot.send_message(self.bot.get_server('197780624688414720').get_channel('332616763294613505'), embed=embed)

def setup(bot):
  bot.add_cog(Misc(bot))

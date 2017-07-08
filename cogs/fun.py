"""
fun, somewhat useful commands
"""

import json
import random

import discord
import requests
from discord.ext import commands


class Fun:

  def __init__(self, bot_):
    self.bot = bot_
    self._8ball_responses = ['Signs point to yes.', 'Yes.', 'Reply hazy, try again.', 'My sources say no.', 'You may rely on it.', 'Concentrate and ask again.', 'Outlook not so good.', 'It is decidedly so.',
                             'Better not tell you now.', 'Very doubtful.', 'Yes - definitely.', 'It is certain.', 'Cannot predict now.', 'Most likely.', 'Ask again later.', 'My reply is no.', 'Outlook good.', "Don't count on it."]
    with open('config.json') as file_in:
      self.config = json.load(file_in)

  def update_config(self):
    with open('config.json', 'r') as file_in:
      self.config = json.load(file_in)

  def module_check(self, context):
    self.update_config()
    for server in self.config['servers']:
      if server['id'] == context.message.server.id:
        if "Fun" in server['enabled_modules']:
          return True
    return False

  @commands.command(name="8ball", pass_context=True)
  async def _8ball_command(self, ctx, *message):
    if not self.module_check(ctx): return
    embed = discord.Embed(title=":8ball:" + ' '.join(message),
                          description=random.choice(self._8ball_responses))
    await self.bot.say(embed=embed)

  @commands.command(name="say", pass_context=True)
  async def say(self, ctx, *message):
    if not self.module_check(ctx): return
    if ctx.message.author.id in self.config['admin_ids']:
      await self.bot.say(' '.join(message))
    else:
      await self.bot.say(ctx.message.author.mention + " said: " + ' '.join(message))

  @commands.command(name="urban", pass_context=True)
  async def urban_dictionary(self, ctx, *message):
    if not self.module_check(ctx): return
    r = requests.get(
        "http://api.urbandictionary.com/v0/define?term={}".format(' '.join(message)))
    r = json.loads(r.text)
    try:
      embed = discord.Embed(title="**Definition for {}**".format(
          r['list'][0]['word']), description=r['list'][0]['definition'], url=r['list'][0]['permalink'])
    except IndexError:
      await self.bot.say('Definition not found for "{}"'.format(' '.join(message)))
    else:
      embed.set_thumbnail(url="http://i.imgur.com/FoxWu8z.jpg")
      embed.add_field(
          name="Example", value=r['list'][0]['example'], inline=False)
      embed.add_field(name="Author", value=r['list'][0]['author'], inline=True)
      embed.add_field(name="Rating", value=":thumbsup: `{}` :thumbsdown: `{}`".format(
          r['list'][0]['thumbs_up'], r['list'][0]['thumbs_down']), inline=True)
      embed.add_field(name="Tags", value=' '.join(r['tags']), inline=False)
      await self.bot.say(embed=embed)

  @commands.command(name="xkcd", pass_context=True)
  async def get_xkcd(self, ctx, number = "random"):
    """
    Retrieves a xkcd comic, from a number, random, or latest

    xkcd <number> for that xkcd number
    xkcd random for a random xkcd
    xkcd latest for the latest xkcd
    """
    if not self.module_check(ctx): return
    if number == "latest":
      r = requests.get('https://xkcd.com/info.0.json')
    elif number == "random":
      r = requests.get('https://xkcd.com/info.0.json')
      r = json.loads(r.text)
      random_xkcd = random.randint(0, r['num'])
      r = requests.get('http://xkcd.com/{}/info.0.json'.format(random_xkcd))
    else:
      r = requests.get('http://xkcd.com/{}/info.0.json'.format(number))
      if r.status_code == 404:
        await self.bot.say("Invalid xkcd number.")
        return
    r = json.loads(r.text)
    embed = discord.Embed(title=r['safe_title'], description=r['alt'], url="https://xkcd.com/{}".format(r['num']))
    embed.set_image(url=r['img'])
    await self.bot.say(embed=embed)

  @commands.command(name="neko", pass_context=True)
  async def nekos(self, ctx):
    if not self.module_check(ctx): return
    r = requests.get('https://nekos.life/api/neko')
    r = .json.loads(r.text)
    embed = discord.Embed()
    embed.set_image(url=r['neko'])
    await self.bot.say(embed=embed)


def setup(bot):
  bot.add_cog(Fun(bot))

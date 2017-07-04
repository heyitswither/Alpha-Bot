"""
fun, not useful commands
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

  @commands.command(name="8ball")
  async def _8ball_command(self, *message):
    embed = discord.Embed(title=":8ball:" + ' '.join(message),
                          description=random.choice(self._8ball_responses))
    await self.bot.say(embed=embed)

  @commands.command(name="say", pass_context=True)
  async def say(self, ctx, *message):
    if ctx.message.author.id in self.config['admin_ids']:
      await self.bot.say(' '.join(message))
    else:
      await self.bot.say(ctx.message.author.mention + "said: " + ' '.join(message))

  @commands.command(name="urban", pass_context=True)
  async def urban_dictionary(self, ctx, *message):
    r = requests.get(
        "http://api.urbandictionary.com/v0/define?term={}".format(' '.join(message)))
    r = json.loads(str(r.content))
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


def setup(bot):
  bot.add_cog(Fun(bot))

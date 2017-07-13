import discord
import requests
from discord.ext import commands

class NSFW:
  def __init__(self, bot_):
    self.bot = bot_

  def update_config(self):
    with open('config.json', 'r') as file_in:
      self.config = json.load(file_in)

  def module_check(self, context):
    self.update_config()
    for server in self.config['servers']:
      if server['id'] == context.message.server.id:
        if "nsfw" in server['enabled_modules']:
          return True
    return False

  @commands.command(name="nya", pass_context=True)
  async def nya(self, ctx):
    if not self.module_check(ctx): return
    if not ctx.message.channel.name.startswith('nsfw'): return
    r = requests.get('https://nekos.life/api/lewd/neko')
    r = json.loads(r.text)
    embed = discord.Embed()
    embed.set_image(url=r['neko'])
    await self.bot.say(embed=embed)

def setup(bot):
  bot.add_cog(NSFW(bot))

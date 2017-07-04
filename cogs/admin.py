"""
tools for the bot admin
"""

import discord
from discord.ext import commands
import os

class Admin:
  def __init__(self, bot_):
    self.bot = bot_

  @commands.command(name="gitpull", hidden=True)
  async def gitpull(self):
    os.popen("git pull origin master")
    self.bot.say("Done!")

  @commands.command(name="restart", hidden=True)
  async def restart(self):
    self.bot.say("Restarting bot...")
    python = sys.executable
    os.execl(python, python, * sys.argv)

  @commands.command(name="stop", hidden=True)
  async def stop(self):
    self.bot.say("Stopping bot...")
    sys.exit()

def setup(bot):
  bot.add_cog(Admin(bot))

class Welcome:
  def __init__(self, bot_):
    self.bot = bot_

def setup(bot):
  bot.add_cog(Welcome(bot))

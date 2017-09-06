import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import pathvalidate
import requests
import os

class Welcome:

  def __init__(self, bot):
    self.bot = bot


  async def on_member_join(self, member):
    template = Image.open('extras/template.png')
    draw = ImageDraw.Draw(template)
    user = member.name
    server = member.server.name
    img_fraction = 0.50
    fontsize = 16
    member_name = pathvalidate.sanitize_filename(
        member.name).replace('(', '').replace(')', '').replace(' ', '')
    server_name = pathvalidate.sanitize_filename(
        member.server.name).replace('(', '').replace(')', '').replace(' ', '')
    if member.avatar_url == "":
      member_avatar = requests.get(member.default_avatar_url)
    else:
      member_avatar = requests.get(member.avatar_url)
    with open('extras/{}.png'.format(member_name), 'wb') as f:
      for chunk in member_avatar.iter_content(chunk_size=1024):
        if chunk:
          f.write(chunk)
    member_avatar = Image.open('extras/{}.png'.format(member_name))
    member_avatar = member_avatar.resize((182, 182), Image.ANTIALIAS)
    template.paste(member_avatar, (34, 71))
    guild_icon = requests.get(member.server.icon_url)
    with open('extras/{}.png'.format(server_name), 'wb') as f:
      for chunk in guild_icon.iter_content(chunk_size=1024):
        if chunk:
          f.write(chunk)
    guild_icon = Image.open('extras/{}.png'.format(server_name))
    guild_icon = guild_icon.resize((64, 64), Image.ANTIALIAS)
    template.paste(guild_icon, (660, 300))
    font = ImageFont.truetype("extras/segoeui.ttf", fontsize)
    while font.getsize(user)[0] < img_fraction * template.size[0]:
      fontsize += 1
      font = ImageFont.truetype("extras/segoeui.ttf", fontsize)
    fontsize -= 1
    font = ImageFont.truetype("extras/segoeui.ttf", fontsize)
    if len(user) < 6:
      font = ImageFont.truetype("extras/segoeui.ttf", 58)
    draw.text((125, 290), user, (0, 0, 0), font=font)

    fontsize = 16
    img_fraction = 0.25
    font = ImageFont.truetype("extras/segoeui.ttf", fontsize)
    while font.getsize(server)[0] < img_fraction * template.size[0]:
      fontsize += 1
      font = ImageFont.truetype("extras/segoeui.ttf", fontsize)
    fontsize -= 1
    font = ImageFont.truetype("extras/segoeui.ttf", fontsize)
    if len(server) < 6:
      font = ImageFont.truetype("extras/segoeui.ttf", 32)
    draw.text((540, 255), server, (0, 0, 0), font=font)

    template.save('extras/finished.png')
    await self.bot.send_file(member.server, 'extras/finished.png')
    os.remove('extras/finished.png')
    os.remove('extras/{}.png'.format(member_name))
    os.remove('extras/{}.png'.format(server_name))

def setup(bot):
  bot.add_cog(Welcome(bot))

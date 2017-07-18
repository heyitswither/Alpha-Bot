"""
bot info, server info, user info, any other info; all goes here
"""

from datetime import datetime
from platform import python_version

import discord
import requests
from discord.ext import commands


class Info:
  def __init__(self, bot_):
    self.bot = bot_

  def get_status(self, user):
    if user.status.online:
      return "Online"
    elif user.status.offline:
      return "Offline"
    elif user.status.idle:
      return "Idle"
    elif user.status.dnd:
      return "Do not disturb"

  def get_permissions(self, user):
    permissions = []
    if user.server_permissions.administrator:
      permissions.append("Administrator")
      return permissions
    if user.server_permissions.ban_members:
      permissions.append("Ban Members")
    if user.server_permissions.kick_members:
      permissions.append("Kick Members")
    if user.server_permissions.manage_server:
      permissions.append("Manage Server")
    if user.server_permissions.manage_channels:
      permissions.append("Manage Channels")
    if user.server_permissions.manage_roles:
      permissions.append("Manage Roles")
    if user.server_permissions.manage_webhooks:
      permissions.append("Manage Webhooks")
    if user.server_permissions.manage_nicknames:
      permissions.append("Manage Nicknames")
    if user.server_permissions.manage_emojis:
      permissions.append("Manange Emojis")
    if user.server_permissions.view_audit_logs:
      permissions.append("View Audit Logs")
    return permissions

  def get_region(self, server):
    if server.region == discord.ServerRegion.us_west:
      return "us-west"
    elif server.region == discord.ServerRegion.us_east:
      return "us-east"
    elif server.region == discord.ServerRegion.us_central:
      return "us-central"
    elif server.region == discord.ServerRegion.eu_west:
      return "eu-west"
    elif server.region == discord.ServerRegion.eu_central:
      return "eu-central"
    elif server.region == discord.ServerRegion.singapore:
      return "singapore"
    elif server.region == discord.ServerRegion.london:
      return "london"
    elif server.region == discord.ServerRegion.sydney:
      return "sydney"
    elif server.region == discord.ServerRegion.amsterdam:
      return "amsterdam"
    elif server.region == discord.ServerRegion.frankfurt:
      return "frankfurt"
    elif server.region == discord.ServerRegion.brazil:
      return "brazil"
    elif server.region == discord.ServerRegion.vip_us_east:
      return "vip-us-east"
    elif server.region == discord.ServerRegion.vip_us_west:
      return "vip-us-west"
    elif server.region == discord.ServerRegion.vip_amsterdam:
      return "vip-amsterdam"
    return "None"

  @commands.command(name="info")
  async def bot_info(self):
    info_embed = discord.Embed()
    info_embed.set_author(
        name="Alpha Bot", url="https://discord.io/wither", icon_url=self.bot.user.avatar_url)

    info_embed.add_field(
        name="Description", value="The everything in one discord bot.", inline=False)
    info_embed.add_field(
        name="GitHub", value="https://github.com/heyitswither/Alpha-Bot", inline=False)
    info_embed.add_field(
        name="Donate", value="https://paypal.me/WitheredAway", inline=False)
    info_embed.add_field(
        name="Python", value="[{}](https://www.python.org/)".format(python_version(), inline=False))
    info_embed.add_field(
        name="Discord.py", value="[{}](https://github.com/Rapptz/discord.py)".format(discord.__version__), inline=True)
    info_embed.add_field(name="Bot Guilds", value=len(
        self.bot.servers), inline=True)
    members = 0
    for member in self.bot.get_all_members():
      members += 1
    info_embed.add_field(name="Bot Users", value=members, inline=True)
    info_embed.add_field(name="Bot Version", value=self.bot.version, inline=True)
    info_embed.add_field(
        name="Bot Author", value="heyitswither#4340", inline=True)
    info_embed.set_thumbnail(url=self.bot.user.avatar_url + "?size=128x128")
    await self.bot.say(embed=info_embed)

  @commands.command(name="serverinfo", pass_context=True)
  async def server_info(self, ctx,):
    server = ctx.message.server
    embed = discord.Embed()
    embed.set_author(name=server.name, icon_url=server.icon_url)
    embed.set_thumbnail(url=server.icon_url)
    embed.add_field(name="ID", value=server.id)
    embed.add_field(name="Region", value=self.get_region(server))
    embed.add_field(name="Members", value=f'{len([member for member in server.members if member.status == discord.Status.online])}/{server.member_count}')
    embed.add_field(name="Text Channels", value=len([channel for channel in server.channels if channel.type == discord.ChannelType.text]))
    embed.add_field(name="Voice Channels", value=len([channel for channel in server.channels if channel.type == discord.ChannelType.voice]))
    embed.add_field(name="Roles", value=len(server.roles) - 1)
    embed.add_field(name="Owner", value=f'{server.owner.name}#{server.owner.discriminator}')
    embed.add_field(name="All Roles", value="https://hastebin.com/" + requests.post('https://hastebin.com/documents', data='Roles in ' + server.name + ':\n' + ', '.join([role.name for role in server.roles if not role.name == '@everyone'])).json()['key'])
    try:
      embed.add_field(name="All Members", value="https://hastebin.com/" + requests.post('https://hastebin.com/documents', data=b'Members in ' + server.name.encode('utf-8') + b':\n' + b', '.join([member.name.encode('utf-8') for member in server.members])).json()['key'])
    except:
      pass
    await self.bot.say(embed=embed)

  @server_info.error
  async def serverinfo_error(self, error, ctx):
    pass

  @commands.command(name="userinfo", pass_context=True)
  async def user_info(self, ctx, user: discord.User=None):
    if user is None:
      user = ctx.message.author
    embed = discord.Embed(colour=user.colour)
    if user.bot:
      embed.set_author(name=f"{user.name}#{user.discriminator} [BOT]", icon_url=user.avatar_url)
    else:
      embed.set_author(name=f"{user.name}#{user.discriminator}", icon_url=user.avatar_url)
    embed.set_thumbnail(url=user.avatar_url)
    embed.add_field(name="ID", value=user.id)
    embed.add_field(name="Status", value=self.get_status(user))
    embed.add_field(name="Registered", value=datetime.strptime(str(user.created_at).split('.')[0], "%Y-%m-%d %X").strftime("%a, %b %e, %Y %I:%M %p"))
    if user in ctx.message.server.members:
      embed.add_field(name="Joined", value=datetime.strptime(str(user.joined_at).split('.')[0], "%Y-%m-%d %X").strftime("%a, %b %e, %Y %I:%M %p"))
      if not user.game is None:
        embed.add_field(name="Game", value=user.game.name)
      else:
        embed.add_field(name="Game", value="None")
      if not user.nick is None:
        embed.add_field(name="Nickname", value=user.nick)
      else:
        embed.add_field(name="Nickname", value="None")
      if len(user.roles) > 1:
        embed.add_field(name="Roles", value=', '.join([role.name for role in user.roles if not role.name == "@everyone"]))
      if len(self.get_permissions(user)) > 0 and not user == ctx.message.server.owner:
        embed.add_field(name="Permissions", value=', '.join(self.get_permissions(user)))
      elif user == ctx.message.server.owner:
        embed.add_field(name="Permissions", value="Owner")
    await self.bot.say(embed=embed)

  @user_info.error
  async def userinfo_error(self, error, ctx):
    await self.bot.say(str(error))

  @commands.command(name="invite")
  async def bot_invite(self):
    await self.bot.say("You can invite me to your server using this link :smile:\n<{}>".format(discord.utils.oauth_url(self.bot.user.id) + "&permissions=201354247"))

  @commands.command(name="suggest", pass_context=True)
  async def suggest(self, ctx, *suggestion):
    """
    suggest a new feature for the bot
    """
    suggestion = ' '.join(suggestion)
    embed = discord.Embed(title="New Suggestion", description=suggestion)
    embed.set_author(name=ctx.message.author.name + "#" + ctx.message.author.discriminator + " (" + ctx.message.author.id + ")", icon_url=ctx.message.author.avatar_url)
    await self.bot.send_message(self.bot.get_server('197780624688414720').get_channel('332616763294613505'), embed=embed)

  @commands.command(name="msgowner", pass_context=True)
  async def msg_owner(self, ctx, *msg):
    """
    Sends a message to the bot owner
    """
    msg = ' '.join(msg)
    embed = discord.Embed(title="New Message", description=msg)
    embed.set_author(name=ctx.message.author.name + "#" + ctx.message.author.discriminator + " (" + ctx.message.author.id + ")", icon_url=ctx.message.author.avatar_url)
    await self.bot.send_message([user for user in self.bot.get_all_members() if user.id == "144630969729679360"][0], embed=embed)


def setup(bot):
  bot.add_cog(Info(bot))

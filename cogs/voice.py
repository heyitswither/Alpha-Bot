import asyncio
import concurrent.futures
import threading
import traceback
from random import shuffle

import discord
import youtube_dl
from discord.ext import commands


class Song:
    def __init__(self, player, message, args=None, loop=False):
        self.player = player

        if player:
            self.title = self.player.title
            self.url = self.player.url
            self._duration = self.player.duration
        else:
            self.title = args[0]
            self.url = args[1]
            self._duration = 0

        self.message = message
        self.user = message.author
        self.channel = message.channel

        self.loop = loop

        try:
            m, s = divmod(self._duration, 60)
            h, m = divmod(m, 60)

            if h:
                self.duration = " ({}:{}:{})".format(h, m, s)
            elif m:
                self.duration = " ({}:{})".format(m, s)
            else:
                self.duration = " ({})".format(s)
        except TypeError:
            self.duration = None
            self.title = self.url.split("/")[2].split(":")[0]

        if self.duration == "(0)":
            self.duration = ""


class VoiceClient:
    def __init__(self, channel, bot_):
        self.bot = bot_

        self.channel = channel
        self.server = channel.server

        self.current_song = None
        self.player = None
        self.volume = 0.2
        self.queue = []

        self.loop = self.bot.loop.create_task(self.main_loop())

    @property
    def client(self):
        return self.bot.voice_client_in(self.server)

    async def play_next_in_queue(self):
        options = {
            'default_search': 'auto',
            'quiet': True,
            'ignoreerrors': True,
        }
        try:
            song = self.queue[0]
            if not song.loop:
                del self.queue[0]
        except IndexError:
            print("error: Nothing next in queue")
            return None

        if not [user for user in self.channel.voice_members if not user.bot]:  # butty is alone :'c
            # self.loop.cancel()
            await self.client.disconnect()
            self.queue = []
            self.player.stop()
            del self.bot.cogs['Voice'].voice_clients[self.server.id]
            raise concurrent.futures.CancelledError

        self.player = await self.client.create_ytdl_player(song.url, ytdl_options=options)
        self.player.is_paused = False
        self.player.volume = self.volume
        self.current_song = Song(self.player, song.message)

        await self.bot.send_message(self.current_song.channel, "now playing `{}`{}".format(
            self.current_song.title, self.current_song.duration))

        self.player.start()

    async def add_to_queue(self, name, message, loop=False, playlist=''):
        options = {
            'default_search': 'auto',
            'quiet': True,
            'ignoreerrors': True,
            # 'skip_download': True,
        }

        if not self.client:
            try:
                await self.bot.join_voice_channel(self.channel)
            except concurrent.futures._base.TimeoutError:
                await self.bot.say(
                    "Well, that's an error. I _think_ doing [l will fix it, though\nFeel free to contact me about this")

        if not playlist:
            player = await self.client.create_ytdl_player(name, ytdl_options=options, before_options='-help')
            args = []
        else:
            player = None
            args = [playlist, name]  # title, url (don't ask, rewrite)

        song = Song(player, message,
                    args=args, loop=loop)

        song.player = None
        self.queue.append(song)

        if not playlist and self.player and self.player.is_playing():
            await self.bot.send_message(song.channel, "`{}` added to queue {}".format(song.title, song.duration))

    async def main_loop(self):
        while True:
            try:
                await asyncio.sleep(1)
                if self.queue and (not self.player or (not self.player.is_playing() and not self.player.is_paused)):
                    await self.play_next_in_queue()
            except concurrent.futures.CancelledError:
                break
            except Exception as e:
                print(''.join(traceback.format_exception(type(e), e, e.__traceback__)))


class Voice:
    def __init__(self, bot_):
        if not discord.opus.is_loaded():
          discord.opus.load_opus("extras/opus.so")
        self.bot = bot_
        self.voice_clients = {}
        if self.bot.voice_reload_cache is not None:
            self.voice_clients = self.bot.voice_reload_cache.copy()
            self.bot.voice_reload_cache = None

    def __unload(self):
        self.bot.voice_reload_cache = self.voice_clients

    @commands.command(name="play", aliases=['add', 'p'], pass_context=True)
    async def voice_play(self, context, *song: str):
        """Search for and play something

        Examples:
          play relaxing flute sounds
          play https://www.youtube.com/watch?v=y_gknRMZ-OU
        """
        if not song:
            context.invoked_with = "help"
            await commands.bot._default_help_command(context, "play")
        message = context.message

        voice = self.voice_clients.get(message.server.id)

        if not voice or not voice.client:
            if message.author.voice_channel:
                voice = VoiceClient(message.author.voice_channel, self.bot)
                self.voice_clients[message.server.id] = voice
            else:
                await self.bot.say("You aren't connected to a voice channel")
                return

        await voice.add_to_queue(' '.join(song), message)

    @commands.command(name="stop", aliases=['skip', 's'], pass_context=True)
    async def voice_stop(self, context):
        """Skips the currently playing song"""
        voice = self.voice_clients.get(context.message.server.id)
        if not voice or not voice.player or not voice.player.is_playing():
            await self.bot.say("B-b-but I haven't even got started... (use [play)")
            return

        if voice.current_song.user != context.message.author:
            await self.bot.say("You can't stop the music~~\n(you're not the person who put this on)")
            return None
        voice.player.stop()

    @commands.command(name="queue", aliases=['q'], pass_context=True)
    async def voice_queue(self, context):
        """Show the songs currently in the queue

        Because discord only allows 2000 characters per message,
        sometimes not all songs in the queue can be shown"""
        message = context.message

        voice = self.voice_clients.get(message.server.id)
        if not voice:
            await self.bot.say("You haven't queued anything yet (use [play)")
            return None

        reply = "Current queue:"
        counter = 1
        for song in voice.queue:
            reply += "\n{}: `{}` {}".format(counter, song.title, song.duration)
            counter += 1
        await self.bot.say(reply)

    @commands.command(name="remove", aliases=['qr'], pass_context=True)
    async def voice_remove(self, context, number):
        voice = self.voice_clients.get(context.message.server.id)
        if not voice:
            await self.bot.say("I removed the silence, but it just keeps coming back (use [play)")
            return

        song = voice.queue[int(number) - 1]
        if song.user != context.message.author:
            await self.bot.say("You can't stop the music~~\n(you're not the person who put this on)")
            return None
        await self.bot.say("Removed `{}` from the queue".format(song.title))
        del voice.queue[int(number) - 1]

    @commands.command(name="playing", aliases=['cp', 'pl'], pass_context=True)
    async def voice_playing(self, context):
        voice = self.voice_clients.get(context.message.server.id)
        if not voice:
            await self.bot.say("Now playing: `John Cage's 4'33` (jk, use [play)")
            return

        song = voice.current_song
        await self.bot.say("now playing `{}` {}".format(song.title, song.duration))

    @commands.command(name="leave", aliases=['l'], pass_context=True)
    async def voice_leave(self, context):
        voice = self.voice_clients.get(context.message.server.id)
        if not voice:
            await self.bot.say("Can't leave if I've never joined (use [play)")
            return

        if voice.player and voice.player.is_playing():
            for song in voice.queue:
                if song.user != context.message.author:
                    await self.bot.say("You can't stop the music~~\n(someone else still has something queued)")
                    return None
            if voice.current_song.user != context.message.author:
                await self.bot.say("You can't stop the music~~\n(someone else is playing something)")
                return None

        voice.loop.cancel()
        await voice.client.disconnect()
        voice.queue = []
        voice.player.stop()
        del self.voice_clients[context.message.server.id]

    @commands.command(name="loop", aliases=['loopadoop'], pass_context=True)
    async def voice_loop(self, context):
        voice = self.voice_clients.get(context.message.server.id)
        if not voice:
            await self.bot.say("Don't worry, the currently playing silence is already looping (use [play)")
            return
        await voice.add_to_queue(voice.current_song.url, context.message, True)

    @commands.command(name="volume", aliases=['v'], pass_context=True)
    async def voice_volume(self, context, volume: int):
        voice = self.voice_clients.get(context.message.server.id)
        if not voice:
            await self.bot.say("Can't change the volume of nothing (use [play)")
            return

        if voice.current_song.user != context.message.author and volume < 20:
            await self.bot.say("You can't change the volume rn, it's not your song")
            return
        voice.volume = volume / 100
        voice.player.volume = volume / 100

    @commands.command(name="playlist", aliases=['pp'], pass_context=True)
    async def voice_playlist(self, context, *song: str):
        song = ' '.join(song)
        message = context.message

        voice = self.voice_clients.get(message.server.id)
        if not voice or not voice.client:
            if message.author.voice_channel:
                voice = VoiceClient(message.author.voice_channel, self.bot)
                self.voice_clients[message.server.id] = voice
            else:
                await self.bot.say("You aren't connected to a voice channel")
                return

        await self.bot.say("Adding playlist; this might take a while")
        info = []
        t = threading.Thread(target=get_playlist_info, args=(song, info))
        t.start()

        while not info:
            await asyncio.sleep(0.5)

        if isinstance(info[0], str):
            await self.bot.say(info[0])

        for x in info[0]['entries']:
            url = "https://www.youtube.com/watch?v=" + x["url"]
            await voice.add_to_queue(url, message, playlist=x['title'])

        await self.bot.say("Playlist successfully added to queue")

    @commands.command(name="shuffle", aliases=['sh'], pass_context=True, hidden=True)
    async def voice_shuffle(self, context):
        voice = self.voice_clients.get(context.message.server.id)
        if not voice:
            await self.bot.say("I can do a dance, but there's nothing in the queue (use [play)")
            return
        shuffle(voice.queue)
        await self.bot.say("Queue shuffled")

    @commands.command(name="pause", pass_context=True)
    async def voice_pause(self, context):
        voice = self.voice_clients.get(context.message.server.id)
        if not voice or not voice.player:
            await self.bot.say(
                "Wow you sure have nothing playing right now\nwhy would you pause nothign\nthat doesn't make any sense")
            return
        voice.player.pause()
        voice.player.is_paused = True
        await self.bot.say("paused, probably")

    @commands.command(name="resume", aliases=['unpause'], pass_context=True, hidden=True)
    async def voice_unpause(self, context):
        voice = self.voice_clients.get(context.message.server.id)
        if not voice or not voice.player:
            await self.bot.say("DW nothing was paused to begin with")
            return
        voice.player.resume()
        voice.player.is_paused = False
        await self.bot.say("unpaused, probably")


def get_playlist_info(song, info):
    ydl = youtube_dl.YoutubeDL({"extract_flat": True, 'quiet': True})
    try:
        info.append(ydl.extract_info(song, download=False))
    except youtube_dl.utils.DownloadError:
        info.append("You need to give the exact url of the playlist")


def setup(bot):
    bot.add_cog(Voice(bot))

    # Todo:
    # Fix any bugs that pop up
    # Pause/resume

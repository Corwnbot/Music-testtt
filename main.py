import discord
from discord.ext import commands
import youtube_dl

bot = commands.Bot(command_prefix='!')

class MusicPlayer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []
        self.is_playing = False

    async def play_music(self, ctx):
        if not self.queue:
            self.is_playing = False
            return

        self.is_playing = True

        voice_channel = ctx.author.voice.channel
        if not ctx.voice_client:
            voice_client = await voice_channel.connect()
        else:
            voice_client = ctx.voice_client

        while self.queue:
            url = self.queue.pop(0)
            with youtube_dl.YoutubeDL({'format': 'bestaudio'}) as ydl:
                info = ydl.extract_info(url, download=False)
                url2 = info['formats'][0]['url']
                voice_client.play(discord.FFmpegPCMAudio(url2), after=lambda e: print('done', e))
                await ctx.send(f'Now playing: {info["title"]}')
                while voice_client.is_playing():
                    await asyncio.sleep(1)
        
        voice_client.stop()
        await voice_client.disconnect()

    @commands.command()
    async def play(self, ctx, *, url):
        self.queue.append(url)
        if not self.is_playing:
            await self.play_music(ctx)

    @commands.command()
    async def pause(self, ctx):
        voice_client = ctx.voice_client
        if voice_client.is_playing():
            voice_client.pause()

    @commands.command()
    async def resume(self, ctx):
        voice_client = ctx.voice_client
        if voice_client.is_paused():
            voice_client.resume()

    @commands.command()
    async def skip(self, ctx):
        voice_client = ctx.voice_client
        if voice_client.is_playing():
            voice_client.stop()

    @commands.command()
    async def stop(self, ctx):
        voice_client = ctx.voice_client
        if voice_client.is_playing():
            self.queue = []
            voice_client.stop()
            await voice_client.disconnect()

    @commands.command()
    async def queue(self, ctx):
        if self.queue:
            await ctx.send('Queue:')
            for i, url in enumerate(self.queue):
                await ctx.send(f'{i+1}. {url}')
        else:
            await ctx.send('Queue is empty.')

@bot.event
async def on_ready():
    print('Bot is ready.')

bot.add_cog(MusicPlayer(bot))
bot.run('MTIxMjg4Mzk5Njk2NzU2NzQwMg.GDH1Wr.meJw4ePLfIZKFdZxKw9e1C9CnoWIN0AnLIXIQM')

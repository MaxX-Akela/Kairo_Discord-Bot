import disnake
from disnake.ext import commands
import wavelink

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            if ctx.voice_client is None:
                await channel.connect(cls=wavelink.Player)
                await ctx.send(f"Подключился к {channel.name}")
            else:
                await ctx.send("Я уже подключен к каналу.")
        else:
            await ctx.send("Вы должны быть в голосовом канале.")

    @commands.command()
    async def leave(self, ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("Отключился от канала.")
        else:
            await ctx.send("Я не подключен к голосовому каналу.")

    @commands.command()
    async def play(self, ctx, *, query: str):
        if not ctx.voice_client:
            return await ctx.send("Сначала подключитесь к голосовому каналу с !join")

        player = ctx.voice_client
        tracks = await wavelink.YouTubeTrack.search(query)
        
        if not tracks:
            return await ctx.send("Трек не найден.")

        await player.play(tracks[0])
        await ctx.send(f"Играю: {tracks[0].title}")

    @commands.command()
    async def stop(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            await ctx.voice_client.stop()
            await ctx.send("Остановил воспроизведение.")
        else:
            await ctx.send("Ничего не играет.")

def setup(bot):
    bot.add_cog(Music(bot))

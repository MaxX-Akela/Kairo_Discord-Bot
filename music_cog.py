import disnake
from disnake.ext import commands
import wavelink

class MusicCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.wavelink = wavelink.Client(self.bot)
        await self.bot.wavelink.initiate_node(
            host='192.168.1.125',
            port=2333,
            rest_uri='http://localhost:2333',
            password='akela',  # Убедитесь, что этот пароль совпадает с конфигурацией Lavalink
            identifier='MAIN',
            region='eu'
        )

    @commands.slash_command(description="Присоеденение бота в канал")
    async def join(self, inter: disnake.AppCmdInter):
        """Присоединиться к голосовому каналу."""
        if inter.author.voice:
            channel = inter.author.voice.channel
            await channel.connect(cls=wavelink.AudioNode)
            await inter.response.send_message(f'Подключен к {channel.name}')
        else:
            await inter.response.send_message("Вы не находитесь в голосовом канале.")

    @commands.slash_command(description="Выход бота из канала")
    async def leave(self, inter: disnake.AppCmdInter):
        """Покинуть голосовой канал."""
        if inter.guild.voice_client:
            await inter.guild.voice_client.disconnect()
            await inter.response.send_message("Отключился от голосового канала.")
        else:
            await inter.response.send_message("Я не в голосовом канале.")

    @commands.slash_command(description="Начать воспроизвдение")
    async def play(self, inter: disnake.AppCmdInter, url: str):
        """Воспроизвести музыку по ссылке."""
        if not inter.guild.voice_client:
            await inter.response.send_message("Я не подключен к голосовому каналу. Используйте команду /join.")
            return

        player = inter.guild.voice_client
        
        # Ищем трек
        track = await self.bot.wavelink.get_tracks(url)
        if not track:
            await inter.response.send_message("Не удалось найти трек.")
            return
        
        await player.play(track[0])
        await inter.response.send_message(f"Воспроизведение: {track[0].title}")

    @commands.slash_command(description="Остановить воспризведение")
    async def stop(self, inter: disnake.AppCmdInter):
        """Остановить воспроизведение музыки."""
        if inter.guild.voice_client and inter.guild.voice_client.is_playing():
            await inter.guild.voice_client.stop()
            await inter.response.send_message("Музыка остановлена.")
        else:
            await inter.response.send_message("Я не воспроизводлю музыку.")

def setup(bot: commands.Bot):
    bot.add_cog(MusicCog(bot))

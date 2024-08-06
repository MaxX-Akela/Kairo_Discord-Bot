import disnake
from disnake.ext import commands

class LogsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command()
    async def recent_messages(self, inter: disnake.AppCmdInter, channel: disnake.TextChannel):
        """Просмотр последних сообщений в указанном канале."""
        messages = await channel.history(limit=5).flatten()  # Получаем последние 5 сообщений
        if not messages:
            await inter.response.send_message("Нет сообщений в этом канале.")
            return

        embed = disnake.Embed(title=f"Последние сообщения в #{channel.name}", color=0x00ff00)
        for msg in messages:
            embed.add_field(name=f"{msg.author.name}:", value=msg.content[:1024], inline=False)
        
        await inter.response.send_message(embed=embed)

    @commands.slash_command()
    async def server_info(self, inter: disnake.AppCmdInter):
        """Информация о сервере."""
        guild = inter.guild
        embed = disnake.Embed(title=guild.name, color=0x00ff00)
        embed.add_field(name="ID", value=guild.id)
        embed.add_field(name="Количество участников", value=guild.member_count)
        embed.add_field(name="Создан", value=guild.created_at.strftime("%Y-%m-%d %H:%M:%S"))
        
        await inter.response.send_message(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(LogsCog(bot))

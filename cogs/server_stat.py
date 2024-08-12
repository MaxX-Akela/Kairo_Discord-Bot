import disnake
from disnake.ext import commands

class server(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

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
    bot.add_cog(server(bot))

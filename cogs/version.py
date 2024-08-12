import disnake
import sys
from disnake.ext import commands

class VersionBot(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(description="Узнайте версии библиотек и Python")
    async def version(self, inter: disnake.ApplicationCommandInteraction):
        # Получаем версии библиотек
        python_version = sys.version
        disnake_version = disnake.__version__

        embed = disnake.Embed(
            title="Версии библиотек",
            description=f"Python: {python_version}\nDisnake: {disnake_version}",
            color=disnake.Color.blue()
        )
        
        await inter.response.send_message(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(VersionBot(bot))
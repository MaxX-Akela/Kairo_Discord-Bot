import disnake
from disnake.ext import commands


class PingCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(description="Узнай задержку бота")
    async def ping(self, inter: disnake.ApplicationCommandInteraction):
        latency = round(self.bot.latency * 1000)
        embed = disnake.Embed(title="Понг!", description=f"Задержка: {latency} мс", color=disnake.Color.blue())
        await inter.response.send_message(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(PingCommand(bot))

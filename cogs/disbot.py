import disnake
from disnake.ext import commands

bot = commands.Bot(command_prefix="!", intents=disnake.Intents.default())

class disbot(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(description="Дискорд канал бота")
    async def server(inter: disnake.ApplicationCommandInteraction):
        await inter.response.send_message(f"Дискорд канал бота: https://discord.gg/ANFkZkAP")
        await inter.response.send_message(
            "Дискорд канал бота",
            components=[
                disnake.ui.Button(label="Дискорд канал бота", style=disnake.ButtonStyle.primary, custom_id="dis"),
            ],
        )

    @bot.listen("on_button_click")
    async def dis(inter: disnake.MessageInteraction):
        if inter.component.custom_id == "dis":
            await inter.response.send_message("https://discord.gg/ANFkZkAP")
    

def setup(bot: commands.Bot):
    bot.add_cog(disbot(bot))
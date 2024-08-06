import disnake
from disnake.ext import commands
from disnake import TextInputStyle

class MyModal(disnake.ui.Modal):
    def __init__(self):
        components = [
            disnake.ui.TextInput(
                label="Name",
                placeholder="Foo Tag",
                custom_id="name",
                style=TextInputStyle.short,
                max_length=500,
            ),
            disnake.ui.TextInput(
                label="Description",
                placeholder="Lorem ipsum dolor sit amet.",
                custom_id="description",
                style=TextInputStyle.paragraph,
            ),
        ]
        super().__init__(title="Create Tag", components=components)

    async def callback(self, inter: disnake.ModalInteraction):
        embed = disnake.Embed(title="Tag Creation")
        for key, value in inter.text_values.items():
            embed.add_field(
                name=key.capitalize(),
                value=value[:1024],
                inline=False,
            )
        await inter.response.send_message(embed=embed)

class TagsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command()
    async def tags(self, inter: disnake.AppCmdInter):
        """Sends a Modal to create a tag."""
        await inter.response.send_modal(modal=MyModal())
        await inter.response.send_modal(modal=MyModal())

def setup(bot: commands.Bot):
    bot.add_cog(TagsCog(bot))

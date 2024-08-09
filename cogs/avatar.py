import disnake
from disnake.ext import commands

class Avatar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Аватарка")
    async def avatar(self, ctx, member: disnake.Member = None):
        if member is None:
            member = ctx.author  # Если пользователь не указан, используем автора сообщения

        embed = disnake.Embed(title=f"Аватар {member.name}", color=disnake.Color.blue())
        embed.set_image(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.set_footer(text=f"ID: {member.id}")

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Avatar(bot))

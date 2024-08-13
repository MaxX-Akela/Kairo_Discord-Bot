import disnake
from disnake.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Забанить участника на сервере")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: disnake.Member, *, reason=None):
        if member.id == ctx.author.id:
            await ctx.send("Вы не можете забанить себя.")
            return

        
        await member.ban(reason=reason)

        
        reasonEmbed = disnake.Embed(
            description=f'Пользователь {member.mention} был забанен.',
            colour=0xFF0000 
        )
        reasonEmbed.add_field(name="Причина:", value=reason if reason else "Не указана")
        reasonEmbed.set_author(name=f"{member.name}#{member.discriminator}", icon_url=str(member.avatar))
        reasonEmbed.set_footer(text=f"Забанен {ctx.author.name}", icon_url=str(ctx.author.avatar))

    
        await ctx.send(embed=reasonEmbed)

def setup(bot):
    bot.add_cog(Moderation(bot))



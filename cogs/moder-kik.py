import disnake
from disnake.ext import commands

class Moder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="kik")
    @commands.has_permissions(kick_members=True)
    async def kik(self, inter, member: disnake.Member, *, reason):
        if member.id == inter.author.id:
            embed = disnake.Embed(
                title="Ошибка!",
                description="Ты не можешь себя кикать!",
                colour=0x0000FF,
            )
            await inter.send(embed=embed)
            return
        
        if member.top_role >= inter.author.top_role:
            embed = disnake.Embed(
                title="Ошибка!",
                description="Вы не можете исключать участников с более высокой ролью!",
                colour=0x0000FF,
            )
            await inter.send(embed=embed)
            return
        
        if member.top_role >= inter.guild.me.top_role:
            embed = disnake.Embed(
                title="Ошибка!",
                description="Роль бота недостаточно высока, чтобы исключить этого участника.",
                colour=0x0000FF,
            )
            await inter.send(embed=embed)
            return
        
        else:
            dmembed = disnake.Embed(
                title="Кик",
                description=f'Тебя выгнали из-за "{reason}", подумай над своим поведением!',
                colour=0x0000FF, 
            )
            
            guild = inter.guild
            
            dmembed.set_thumbnail(url=guild.icon.url if guild.icon else disnake.Embed.Empty)
            dmembed.set_author(
                name=f"{inter.guild}",
            )  
            
            await member.send(embed=dmembed)
            
            await member.kick(reason=reason)
            reasonEmbed = disnake.Embed(
                description=f'Успешно выгнали {member.mention} из-за "{reason}"',
                colour=0x0000FF
            )
            reasonEmbed.set_author(name=f"{member.name}#{member.discriminator}", icon_url='{}'.format(member.avatar))
            reasonEmbed.set_footer(text=f"Выгнан {inter.author.name}", icon_url='{}'.format(inter.author.avatar))
            await inter.send(embed=reasonEmbed)

def setup(bot):
    bot.add_cog(Moder(bot))




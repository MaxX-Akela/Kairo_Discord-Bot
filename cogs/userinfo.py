import disnake
from disnake.ext import commands

class UserInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Информация о пользователе на сервере")
    async def userinfo(self, ctx, member: disnake.Member = None):
        if member is None:
            member = ctx.author  # Если пользователь не указан, используем автора сообщения

        embed = disnake.Embed(title=f"Информация о пользователе: {member.name}", color=0x0000FF)
        embed.add_field(name="ID пользователя", value=member.id, inline=False)
        embed.add_field(name="Имя пользователя", value=member.mention, inline=False)
        embed.add_field(name="Аккаунт создан", value=member.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
        embed.add_field(name="Присоединился к серверу", value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
        
        # Добавляем информацию о статусе и голосовой активности
        
        
        if member.voice:
            embed.add_field(name="В голосовом канале?", value=f"В канале: {member.voice.channel.name}", inline=False)
        else:
            embed.add_field(name="В голосовом канале?", value="Не в голосовом канале", inline=False)

        embed.set_thumbnail(url=member.avatar.url if member.avatar else None)

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(UserInfo(bot))


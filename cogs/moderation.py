import disnake
from disnake.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="kick")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: disnake.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f'Пользователь {member.mention} был кикнут. Причина: {reason}')

    @commands.slash_command(description="ban")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: disnake.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'Пользователь {member.mention} был забанен. Причина: {reason}')

    @commands.slash_command(description="unban")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, user):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = user.split('#')

        for ban_entry in banned_users:
            if (ban_entry.user.name == member_name and
                    ban_entry.user.discriminator == member_discriminator):
                await ctx.guild.unban(ban_entry.user)
                await ctx.send(f'Пользователь {ban_entry.user.mention} был разбанен.')
                return
        await ctx.send(f'Пользователь {user} не найден в бан-листе.')

    @commands.slash_command(description="mute")
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: disnake.Member, *, reason=None):
        mute_role = disnake.utils.get(ctx.guild.roles, name="Muted")
        if not mute_role:
            mute_role = await ctx.guild.create_role(name="Muted")

            for channel in ctx.guild.channels:
                await channel.set_permissions(mute_role, speak=False, send_messages=False)

        await member.add_roles(mute_role, reason=reason)
        await ctx.send(f'Пользователь {member.mention} был замучен. Причина: {reason}')

    @commands.slash_command(description="unmute")
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: disnake.Member):
        mute_role = disnake.utils.get(ctx.guild.roles, name="Muted")
        if mute_role in member.roles:
            await member.remove_roles(mute_role)
            await ctx.send(f'Пользователь {member.mention} был размучен.')
        else:
            await ctx.send(f'Пользователь {member.mention} не замучен.')

def setup(bot):
    bot.add_cog(Moderation(bot))


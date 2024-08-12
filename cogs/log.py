import disnake
from disnake.ext import commands

class AuditLogCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = None  # ID канала для логов

    @commands.slash_command(description="Канал")
    async def setlogchannel(self, ctx, channel: disnake.TextChannel):
        """Установить канал для логов аудита."""
        self.channel_id = channel.id
        await ctx.send(f"Канал для логов установлен: {channel.mention}")

    @commands.slash_command(description="Логи")
    async def auditlogs(self, ctx):
        """Получить последние журналы аудита и отправить их в указанный канал."""
        if self.channel_id is None:
            await ctx.send("Канал для логов не установлен. Используйте /setlogchannel <канал>.")
            return

        log_channel = self.bot.get_channel(self.channel_id)
        if log_channel is None:
            await ctx.send("Указанный канал не найден.")
            return

        # Получаем журналы аудита для сервера
        audit_logs = await ctx.guild.audit_logs(limit=10).flatten()  # Получаем последние 10 записей

        if not audit_logs:
            await log_channel.send("Нет доступных журналов аудита.")
            return

        for entry in audit_logs:
            embed = disnake.Embed(
                title="Журнал аудита",
                description=f"Тип: {entry.action}",
                color=disnake.Color.blue()
            )
            embed.add_field(name="Пользователь", value=str(entry.user), inline=False)
            embed.add_field(name="Дата", value=str(entry.created_at), inline=False)

            await log_channel.send(embed=embed)

# Функция для настройки cog
def setup(bot):
    bot.add_cog(AuditLogCog(bot))


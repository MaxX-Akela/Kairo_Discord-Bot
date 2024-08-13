import disnake
from disnake.ext import commands
import sqlite3

# Создаем подключение к базе данных
conn = sqlite3.connect('levels.db')
c = conn.cursor()

# Создаем таблицу, если она не существует
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    xp INTEGER DEFAULT 0,
    level INTEGER DEFAULT 1
)
''')
conn.commit()

class LevelEmbed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def add_xp(self, user_id, xp):
        c.execute('INSERT OR IGNORE INTO users (user_id) VALUES (?)', (user_id,))
        c.execute('UPDATE users SET xp = xp + ? WHERE user_id = ?', (xp, user_id))
        conn.commit()

    def get_user_data(self, user_id):
        c.execute('SELECT xp, level FROM users WHERE user_id = ?', (user_id,))
        return c.fetchone()

    # Функция для обновления уровня
    def update_level(self, user_id):
        xp, level = self.get_user_data(user_id)
        new_level = int(xp ** 0.5)  # формула для уровня
        if new_level != level:
            c.execute('UPDATE users SET level = ? WHERE user_id = ?', (new_level, user_id))
            conn.commit()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        self.add_xp(message.author.id, 5)  # + 5 XP за сообщение 
        self.update_level(message.author.id) 

    @commands.slash_command(description="Ваш ранг на сервере")
    async def ранг(self, interaction: disnake.ApplicationCommandInteraction):
        user_data = self.get_user_data(interaction.user.id)
        if user_data:
            xp, level = user_data
        else:
            await interaction.send('Вы еще не имеете опыта.')

        embed = disnake.Embed(
            title=f"Ваш уровень:",
            description=f'Level: {level}, XP: {xp}',
            color=0x0000FF,
        )

        await interaction.send(embed=embed)

    @commands.slash_command(description="Лидеры по уровню")
    async def лидеры(self, interaction: disnake.ApplicationCommandInteraction):
        c.execute('SELECT user_id, level FROM users ORDER BY level DESC LIMIT 20')
        leaders = c.fetchall()
        leaderboard = "\n".join([f"<@{user_id}>: Уровень {level}" for user_id, level in leaders])
        await interaction.send(f'Топ 20 по уровням:\n{leaderboard}')


def setup(bot: commands.Bot):
    bot.add_cog(LevelEmbed(bot))
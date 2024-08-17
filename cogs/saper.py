import disnake
from disnake.ext import commands
import random

class Minesweeper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.field_size = 3
        self.bomb_position = None
        self.opened_cells = set()

    @commands.slash_command(name="minesweeper", description="Играйте в Сапёр!")
    async def minesweeper(self, interaction: disnake.ApplicationCommandInteraction):
        self.bomb_position = (random.randint(0, self.field_size - 1), random.randint(0, self.field_size - 1))
        self.opened_cells.clear()
        
        await self.send_board(interaction)

    async def send_board(self, interaction):
        buttons = [
            [disnake.ui.Button(label="🟩", style=disnake.ButtonStyle.secondary, custom_id=f"{i},{j}") 
             for j in range(self.field_size)] 
            for i in range(self.field_size)
        ]

        action_rows = [disnake.ui.ActionRow(*row) for row in buttons]
        await interaction.send("Нажмите на ячейку, чтобы открыть её!", components=action_rows)

        # Ожидаем нажатие кнопки
        interaction_response = await self.bot.wait_for("button_click", check=lambda i: i.user == interaction.user)

        await self.handle_click(interaction_response)

    async def handle_click(self, interaction_response):
        coords = tuple(map(int, interaction_response.component.custom_id.split(',')))
        
        if coords == self.bomb_position:
            await interaction_response.send("💣 Вы попали на бомбу! Игра окончена.", ephemeral=True)
            return

        if coords not in self.opened_cells:
            self.opened_cells.add(coords)

            # Проверяем, остались ли еще безопасные ячейки
            if len(self.opened_cells) == (self.field_size ** 2 - 1):  # 1 бомба
                await interaction_response.send("🎉 Поздравляем! Вы выиграли!", ephemeral=True)
                return

            # Обновляем кнопки
            buttons = [
                [disnake.ui.Button(label="✅" if (i, j) in self.opened_cells else "🟩", style=disnake.ButtonStyle.secondary, custom_id=f"{i},{j}", disabled=(i, j) in self.opened_cells) 
                 for j in range(self.field_size)] 
                for i in range(self.field_size)
            ]

            action_rows = [disnake.ui.ActionRow(*row) for row in buttons]
            await interaction_response.message.edit(components=action_rows)

            # После обработки нажатия, снова ожидаем нажатие кнопки
            await self.send_board(interaction_response)

def setup(bot):
    bot.add_cog(Minesweeper(bot))


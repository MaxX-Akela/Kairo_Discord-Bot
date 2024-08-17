import disnake
from disnake.ext import commands
import random

class RPS(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="rps", description="Играйте в камень, ножницы, бумага!")
    async def rps(self, interaction: disnake.ApplicationCommandInteraction):
        buttons = [
            disnake.ui.Button(label="Камень", style=disnake.ButtonStyle.primary, custom_id="rock"),
            disnake.ui.Button(label="Ножницы", style=disnake.ButtonStyle.red, custom_id="scissors"),
            disnake.ui.Button(label="Бумага", style=disnake.ButtonStyle.green, custom_id="paper"),
        ]

        action_row = disnake.ui.ActionRow(*buttons)
        await interaction.send("Выберите: Камень, Ножницы или Бумага!", components=[action_row])

        # Ожидание ответа от игрока
        interaction_response = await self.bot.wait_for("button_click", check=lambda i: i.user == interaction.user)

        user_choice = interaction_response.component.custom_id
        bot_choice = random.choice(["rock", "scissors", "paper"])
        
        result = self.determine_winner(user_choice, bot_choice)

        await interaction_response.send(f"Вы выбрали: {user_choice}\nБот выбрал: {bot_choice}\nРезультат: {result}")

    def determine_winner(self, user, bot):
        if user == bot:
            return "Ничья!"
        elif (user == "rock" and bot == "scissors") or \
             (user == "scissors" and bot == "paper") or \
             (user == "paper" and bot == "rock"):
            return "Вы выиграли!"
        else:
            return "Вы проиграли!"

def setup(bot):
    bot.add_cog(RPS(bot))

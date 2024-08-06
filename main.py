import disnake
from disnake.ext import commands

bot = commands.Bot(command_prefix="!", intents=disnake.Intents.default())
intents = disnake.Intents.default()
intents.message_content = True

DISCORD_TOKEN = 'TOKEN'

@bot.event
async def on_ready():
    print("          .__          ")
    print("   /| |/  |__ |    /|  ")                  
    print("  /-| |\  |__ |__ /-|  ")
    print("                          lox")
    print(f'Logged in as {bot.user}')
    await bot.change_presence(status=disnake.Status.dnd, activity=disnake.Game("Dota 2( •̀ ω •́ )✧"))


bot.load_extensions('cogs')


bot.run(DISCORD_TOKEN)


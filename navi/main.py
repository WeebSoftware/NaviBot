import disnake
import os
from disnake.ext import commands

DISCORD_TOKEN=os.getenv('DISCORD_TOKEN')

intents = disnake.Intents.default()
intents.message_content = True

bot = commands.InteractionBot(intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello World!')

bot.run(DISCORD_TOKEN)

import disnake
import os
from disnake.ext import commands

DISCORD_TOKEN=os.getenv('DISCORD_TOKEN')

intents = disnake.Intents.default()
intents.message_content = True

command_sync_flags = commands.CommandSyncFlags.default()
command_sync_flags.sync_commands_debug = True

bot = commands.InteractionBot(
    intents=intents,
    command_sync_flags=command_sync_flags
)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello World!')

@bot.slash_command(description="If you know, you know.")
async def lovelain(inter):
    with open(f"{os.path.dirname(__file__)}/images/lovelain.png", "rb") as love_lain_original_file:
        love_lain_response_file = disnake.File(love_lain_original_file)
        love_lain_text = "Let's all love Lain... Let's all love Lain, let's all love Lain, let's all love Lain, LainLainLainLainLainLainLainLainL-l-l-l-l-l!"

        await inter.response.send_message(content=love_lain_text, file=love_lain_response_file)

bot.run(DISCORD_TOKEN)

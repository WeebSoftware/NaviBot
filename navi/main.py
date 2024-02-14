import config
import disnake
import os
from disnake.ext import commands
from openai import OpenAI

# OPENAI
openai_client = OpenAI()
openai_chat_history = []

# API TOKENS
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# INTENTS
intents = disnake.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True

# BOT CREATION
command_sync_flags = commands.CommandSyncFlags.default()
command_sync_flags.sync_commands_debug = True

bot = commands.InteractionBot(intents=intents, command_sync_flags=command_sync_flags)


# EVENT HANDLERS
@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")


@bot.event
async def on_raw_reaction_add(payload):
    # Reaction Roles
    if payload.channel_id != config.REACTION_ROLE_CHANNEL_ID:
        return

    for emoji_raw, role_id in config.EMOJI_RAW_TO_ROLE_ID.items():
        if payload.emoji == disnake.PartialEmoji.from_str(value=emoji_raw):
            guild = bot.get_guild(payload.guild_id)
            if guild == None:
                return

            role = guild.get_role(role_id)
            if role == None:
                return

            await payload.member.add_roles(role)


@bot.event
async def on_raw_reaction_remove(payload):
    # Reaction Roles
    if payload.channel_id != config.REACTION_ROLE_CHANNEL_ID:
        return

    for emoji_raw, role_id in config.EMOJI_RAW_TO_ROLE_ID.items():
        if payload.emoji == disnake.PartialEmoji.from_str(value=emoji_raw):
            guild = bot.get_guild(payload.guild_id)
            if guild == None:
                print("guild not found")
                return

            member = guild.get_member(payload.user_id)
            if member == None:
                print("member not found")
                return

            role = guild.get_role(role_id)
            if role == None:
                print("role not found")
                return

            await member.remove_roles(role)


@bot.slash_command(description="Chat with Navi!")
async def chat(inter, message):
    openai_chat_history.append({"role": "user", "content": message})
    while len(openai_chat_history) > 5:
        openai_chat_history.pop(1)

    completion = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": config.NAVI_CHAT_PROMPT}]
        + openai_chat_history,
    )

    navi_response = completion.choices[0].message.content
    openai_chat_history.append({"role": "assistant", "content": navi_response})

    await inter.response.send_message(content=navi_response)


@bot.slash_command(description="If you know, you know.")
async def lovelain(inter):
    with open(
        f"{os.path.dirname(__file__)}/images/lovelain.png", "rb"
    ) as love_lain_original_file:
        love_lain_response_file = disnake.File(love_lain_original_file)
        love_lain_text = "Let's all love Lain... Let's all love Lain, let's all love Lain, let's all love Lain, LainLainLainLainLainLainLainLainL-l-l-l-l-l!"

        await inter.response.send_message(
            content=love_lain_text, file=love_lain_response_file
        )


@bot.slash_command(
    description="Regenerate the reaction role message in the activated channel",
    default_member_permissions=disnake.Permissions(permissions=8),
)
async def rrmessage(inter):
    embed = disnake.Embed(
        title="Get Your Color Roles Here!",
        description="React with the corresponding emoji to get your color role.",
        color=disnake.Color(value=0xFBE3FF),
    )
    for emoji_raw, role_id in config.EMOJI_RAW_TO_ROLE_ID.items():
        embed.add_field(name=emoji_raw, value=f"<@&{role_id}>")

    await inter.response.send_message(embed=embed)


bot.run(DISCORD_TOKEN)

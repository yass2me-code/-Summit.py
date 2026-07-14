# =========================
# SUMMIT STATE ROLEPLAY BOT
# PART 1 - CONFIG + BOT
# =========================

import discord
from discord.ext import commands, tasks
from discord import app_commands
import aiohttp
import os
import datetime


# =========================
# CONFIG
# =========================

TOKEN = os.getenv("TOKEN")

GUILD_ID = 000000000000000000  # CHANGE THIS
GUILD = discord.Object(id=GUILD_ID)


ERLC_SERVER_KEY = os.getenv("ERLC_SERVER_KEY")


SERVER_NAME = "Summit State Roleplay"
SERVER_CODE = "ssrpp"
SERVER_OWNER = "1221dumtruck"
ERLC_SERVER_KEY = os.getenv("NXGOMWWDAOADYCZrrHsq-haVbGfMwtNMbLWTPhVMMSCnFfnOIxHwukxWuiVjS")

# =========================
# BOT SETUP
# =========================

intents = discord.Intents.default()
intents.message_content = True


bot = commands.Bot(
    command_prefix=["!", "."],
    intents=intents
)


# =========================
# READY
# =========================

@bot.event
async def on_ready():

    print("=========================")
    print(f"Logged in as {bot.user}")
    print("Summit Roleplay Bot Online")
    print("=========================")


    try:

        synced = await bot.tree.sync(
            guild=GUILD
        )

        print(
            f"Synced {len(synced)} slash commands"
        )

    except Exception as e:

        print(
            "Sync error:",
            e
        )


# =========================
# PING COMMAND
# =========================

@bot.tree.command(
    name="ping",
    description="Check bot latency",
    guild=GUILD
)
async def ping(interaction: discord.Interaction):

    await interaction.response.send_message(
        f"🏓 Pong! `{round(bot.latency * 1000)}ms`"
    )


# =========================
# PREFIX TEST
# =========================

@bot.command()
async def test(ctx):

    await ctx.send(
        "✅ Prefix command works"
    )# =========================
# SUMMIT SERVER INFO
# =========================

SERVERINFO_CHANNEL_ID = 1522610008162828338

serverinfo_message = None
update_counter = 0

staff_on_shift = set()


# =========================
# STAFF SHIFT
# =========================

@bot.tree.command(
    name="shift",
    description="Go on staff shift",
    guild=GUILD
)
async def shift(interaction: discord.Interaction):

    staff_on_shift.add(interaction.user.id)

    await interaction.response.send_message(
        "🟢 You are now on shift.",
        ephemeral=True
    )


@bot.tree.command(
    name="shiftoff",
    description="Leave staff shift",
    guild=GUILD
)
async def shiftoff(interaction: discord.Interaction):

    staff_on_shift.discard(interaction.user.id)

    await interaction.response.send_message(
        "🔴 You are now off shift.",
        ephemeral=True
    )


# =========================
# ERLC SERVER INFO
# =========================

async def get_server_info():

    url = "https://api.erlc.gg/v1/server"

    headers = {
        "server-key": ERLC_SERVER_KEY
    }

    async with aiohttp.ClientSession() as session:

        async with session.get(
            url,
            headers=headers
        ) as response:

            if response.status != 200:
                return None

            return await response.json()


# =========================
# CREATE EMBED
# =========================

async def create_server_embed():

    global update_counter

    data = await get_server_info()

    if data:

        players = data.get("CurrentPlayers", 0)
        max_players = data.get("MaxPlayers", 50)
        queue = data.get("Queue", 0)

    else:

        players = 0
        max_players = 50
        queue = 0


    embed = discord.Embed(
        title="Welcome to Summit State Roleplay Session Information!",
        color=discord.Color.blue()
    )

    embed.description = (
        "You can find server information below!\n\n"

        "> **Server Name**\n"
        f"```\n{SERVER_NAME}\n```\n\n"

        "> **Server Code**\n"
        f"```\n{SERVER_CODE}\n```\n\n"

        "> **Server Owner**\n"
        f"```\n{SERVER_OWNER}\n```\n\n"

        "**Session Information**\n\n"

        "> **Players**\n"
        f"```\n{players}/{max_players}\n```\n\n"

        "> **Queue**\n"
        f"```\n{queue}\n```\n\n"

        "> **Currently Moderating**\n"
        f"```\n{len(staff_on_shift)}\n```\n\n"

        "> **Updated**\n"
        f"```\n{update_counter}\n```"
    )

    embed.timestamp = datetime.datetime.now()

    return embed


# =========================
# SERVER INFO COMMAND
# =========================

@bot.tree.command(
    name="serverinfo",
    description="Create Summit server info panel",
    guild=GUILD
)
async def serverinfo(interaction: discord.Interaction):

    global serverinfo_message
    global update_counter

    update_counter = 1

    embed = await create_server_embed()

    serverinfo_message = await interaction.channel.send(
        embed=embed
    )

    await interaction.response.send_message(
        "✅ Server info panel created.",
        ephemeral=True
    )


# =========================
# AUTO UPDATE
# =========================

@tasks.loop(seconds=1)
async def serverinfo_loop():

    global update_counter
    global serverinfo_message

    if serverinfo_message is None:
        return

    update_counter += 1

    if update_counter > 10:
        update_counter = 1

    embed = await create_server_embed()

    await serverinfo_message.edit(
        embed=embed
    )


@serverinfo_loop.before_loop
async def before_serverinfo_loop():

    await bot.wait_until_ready()
# =========================
# ERLC RUN COMMAND
# =========================

async def send_erlc_command(command):

    url = "https://api.erlc.gg/v1/server/command"

    headers = {
        "server-key": ERLC_SERVER_KEY,
        "Content-Type": "application/json"
    }

    data = {
        "command": command
    }

    async with aiohttp.ClientSession() as session:

        async with session.post(
            url,
            headers=headers,
            json=data
        ) as response:

            text = await response.text()

            return response.status, text



@bot.tree.command(
    name="run",
    description="Run an ERLC server command",
    guild=GUILD
)
@app_commands.describe(
    command="Command to run in ERLC"
)
async def run(
    interaction: discord.Interaction,
    command: str
):

    await interaction.response.defer(
        ephemeral=True
    )

    status, response = await send_erlc_command(
        command
    )


    if status == 200:

        embed = discord.Embed(
            title="✅ Command Executed",
            description=f"""
**Command**
# =========================
# START BOT
# =========================

TOKEN = os.getenv("TOKEN")

if TOKEN is None:
    print("❌ ERROR: TOKEN is missing from Railway Variables")
else:
    bot.run(TOKEN)

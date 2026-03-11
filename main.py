import asyncio
import discord
from discord.ext import commands

from config import TOKEN, COMMAND_PREFIX
from database import init_db


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)


@bot.event
async def on_ready():
    print(f"Bot ready: {bot.user} (ID: {bot.user.id})")


async def load_extensions():
    await bot.load_extension("cogs.commands")
    await bot.load_extension("cogs.level")


async def main():
    if not TOKEN:
        raise ValueError("DISCORD_BOT_TOKEN が .env に設定されていません。")

    init_db()

    async with bot:
        await load_extensions()
        await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
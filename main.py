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
    """Bot起動完了時に識別情報を表示する。"""
    print(f"Bot ready: {bot.user} (ID: {bot.user.id})")


@bot.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError):
    """コマンド実行エラーを共通処理する。"""
    # 管理者権限不足時は固定メッセージを返す。
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("このコマンドは管理者のみ使用できます。")
        return

    # 未定義コマンドは無視する。
    if isinstance(error, commands.CommandNotFound):
        return

    # それ以外は上位へ送出してログ化しやすくする。
    raise error


async def load_extensions():
    """利用するCogを読み込む。"""
    await bot.load_extension("cogs.commands")
    await bot.load_extension("cogs.level")


async def main():
    """DB初期化後にBotを起動する。"""
    # トークン未設定は早期に例外化する。
    if not TOKEN:
        raise ValueError("DISCORD_BOT_TOKEN が .env に設定されていません。")

    # テーブル作成など初期化を先に実行する。
    init_db()

    async with bot:
        await load_extensions()
        await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())

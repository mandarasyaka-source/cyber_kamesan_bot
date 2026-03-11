import discord
from discord.ext import commands


class BasicCommands(commands.Cog):
    """基本系コマンドを提供するCog。"""

    def __init__(self, bot: commands.Bot):
        """Botインスタンスを保持する。"""
        self.bot = bot

    @commands.command()
    async def ping(self, ctx: commands.Context):
        """Botの応答確認を行う。"""
        # 疎通確認用の固定レスポンス。
        await ctx.send("pong")

    @commands.command(name="挨拶")
    async def greeting(self, ctx: commands.Context):
        """挨拶メッセージを返す。"""
        # 要件指定の文言を返す。
        await ctx.send("こんにちは、僕はサイバーカメさんです。")


async def setup(bot: commands.Bot):
    """CogをBotへ登録する。"""
    await bot.add_cog(BasicCommands(bot))

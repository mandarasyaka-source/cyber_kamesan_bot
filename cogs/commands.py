import discord
from discord.ext import commands


class BasicCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx: commands.Context):
        """Botの応答確認"""
        await ctx.send("pong")


async def setup(bot: commands.Bot):
    await bot.add_cog(BasicCommands(bot))
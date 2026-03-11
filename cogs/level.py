import discord
from discord.ext import commands

from database import add_points, get_points
from config import LEVEL_ROLE_RULES, LEVEL_ROLE_NAMES


class LevelSystem(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def get_level_from_points(self, points: int) -> int:
        current_level = 1

        for level, required_points in sorted(LEVEL_ROLE_RULES.items()):
            if points >= required_points:
                current_level = level

        return current_level

    async def update_level_role(self, member: discord.Member):
        points = get_points(member.id)
        level = self.get_level_from_points(points)

        target_role_name = LEVEL_ROLE_NAMES.get(level)
        if target_role_name is None:
            return

        guild = member.guild
        target_role = discord.utils.get(guild.roles, name=target_role_name)
        if target_role is None:
            return

        level_roles = []
        for role_name in LEVEL_ROLE_NAMES.values():
            role = discord.utils.get(guild.roles, name=role_name)
            if role is not None:
                level_roles.append(role)

        remove_roles = [
            role for role in level_roles
            if role in member.roles and role != target_role
        ]

        if remove_roles:
            await member.remove_roles(*remove_roles, reason="レベルロール更新")

        if target_role not in member.roles:
            await member.add_roles(target_role, reason="レベルロール更新")

    @commands.command()
    async def addpt(self, ctx: commands.Context, amount: int):
        """自分にポイントを加算するテスト用コマンド"""
        if amount < 0:
            await ctx.send("負のポイントは追加できません。")
            return

        add_points(ctx.author.id, amount)
        await self.update_level_role(ctx.author)

        total = get_points(ctx.author.id)
        level = self.get_level_from_points(total)

        await ctx.send(
            f"{ctx.author.display_name} に {amount}pt 追加しました。\n"
            f"現在のポイント: {total}pt\n"
            f"現在のレベル: Lv.{level}"
        )

    @commands.command()
    async def rank(self, ctx: commands.Context):
        """自分のポイントとレベルを表示"""
        total = get_points(ctx.author.id)
        level = self.get_level_from_points(total)

        await ctx.send(
            f"{ctx.author.display_name} の現在ポイントは {total}pt です。\n"
            f"現在のレベルは Lv.{level} です。"
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(LevelSystem(bot))
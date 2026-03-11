from datetime import timezone

import discord
from discord.ext import commands

from database import add_points, get_points, set_points
from config import LEVEL_ROLE_RULES, LEVEL_ROLE_NAMES


class LevelSystem(commands.Cog):
    """ポイントとレベルロール管理を行うCog。"""

    def __init__(self, bot: commands.Bot):
        """Botインスタンスを保持する。"""
        self.bot = bot

    def get_level_from_points(self, points: int) -> int:
        """ポイントから対応するレベルを求める。"""
        current_level = 1

        # 必要ポイントを満たす最大レベルを採用する。
        for level, required_points in sorted(LEVEL_ROLE_RULES.items()):
            if points >= required_points:
                current_level = level

        return current_level

    async def update_level_role(self, member: discord.Member):
        """ユーザーの現在ポイントに応じてレベルロールを更新する。"""
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
        # レベル管理対象のロール一覧を収集する。
        for role_name in LEVEL_ROLE_NAMES.values():
            role = discord.utils.get(guild.roles, name=role_name)
            if role is not None:
                level_roles.append(role)

        # 対象以外のレベルロールは外す。
        remove_roles = [
            role for role in level_roles
            if role in member.roles and role != target_role
        ]

        if remove_roles:
            await member.remove_roles(*remove_roles, reason="レベルロール更新")

        # 対象ロールが未付与なら追加する。
        if target_role not in member.roles:
            await member.add_roles(target_role, reason="レベルロール更新")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def addpt(self, ctx: commands.Context, amount: int):
        """管理者のみ: 実行者にポイントを加算する。"""
        if amount < 0:
            await ctx.send("負のポイントは追加できません。")
            return

        # ポイント加算後、レベルロールも再判定する。
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
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def update(self, ctx: commands.Context):
        """管理者のみ: 全メンバーのポイントを参加日数ベースで上書き更新する。"""
        now = discord.utils.utcnow()
        updated_count = 0

        # サーバーメンバー全員を順番に処理する。
        for member in ctx.guild.members:
            # Botアカウントは対象外。
            if member.bot:
                continue

            joined_at = member.joined_at
            # 参加日時が取得できない場合はスキップ。
            if joined_at is None:
                continue

            # 念のためnaive datetimeはUTCとして扱う。
            if joined_at.tzinfo is None:
                joined_at = joined_at.replace(tzinfo=timezone.utc)

            # 参加経過日数をポイントとして採用する。
            elapsed_days = (now - joined_at).days
            points = max(elapsed_days, 0)

            # 既存値は上書きする。
            set_points(member.id, points)

            # ポイント変更後にレベルロールを更新する。
            try:
                await self.update_level_role(member)
            except discord.Forbidden:
                # 権限不足でロール更新できない場合は次のユーザーへ。
                continue

            updated_count += 1

        await ctx.send(f"参加日数ベースでポイントを更新しました。更新人数: {updated_count}人")

    @commands.command()
    async def rank(self, ctx: commands.Context):
        """実行者のポイントとレベルを表示する。"""
        total = get_points(ctx.author.id)
        level = self.get_level_from_points(total)

        await ctx.send(
            f"{ctx.author.display_name} の現在ポイントは {total}pt です。\n"
            f"現在のレベルは Lv.{level} です。"
        )


async def setup(bot: commands.Bot):
    """CogをBotへ登録する。"""
    await bot.add_cog(LevelSystem(bot))

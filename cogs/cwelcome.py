import discord
from discord.ext import commands
from datetime import datetime, timedelta

from config import config


class CWelcome(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # メンバーの状態変化を検知するイベント
    @commands.Cog.listener("on_member_update")
    async def on_member_update(self, before: discord.Member, after: discord.Member):

        added_roles_id = [role.id for role in set(after.roles) - set(before.roles)]  # 増えたロールのid一覧
        if config.roles.yuruhorominn in added_roles_id:

            channel = await self.bot.fetch_channel(config.channels.invite)  # ようこそチャンネルを取得
            welcome_embed = discord.Embed(
                description=f"## ゆるホロ鯖へようこそ！\nまずは<#{config.channels.role_set}>で自分の推しロールを設定しましょう(^O^)/",
                color=discord.Color.green()
            )
            welcome_embed.set_footer(text=f"なおこのメッセージは{(datetime.now() + timedelta(days=1)).strftime('%Y/%m/%d %H:%M')}に自動で削除されます。")
            await channel.send(f"{after.mention}さんがやってきました！", embed=welcome_embed, silent=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(CWelcome(bot))

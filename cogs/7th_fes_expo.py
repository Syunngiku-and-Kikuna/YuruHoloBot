# import random
# import string
# from datetime import datetime, timedelta

import discord
from discord import app_commands
from discord.ext import commands

# from config import config
from database import Fes_Expo_7th_db, session3


# class Select(discord.ui.Select):
#     def __init__(self, placeholder: str, options: list[discord.SelectOption], min_values: int, max_values: int, custom_id: str, bot: commands.Bot, message: discord.Message):
#         super().__init__(
#             placeholder=placeholder,
#             options=options,
#             min_values=min_values,
#             max_values=max_values,
#             custom_id=custom_id
#         )
#         self.bot = bot
#         self.message = message

#     async def callback(self, interaction: discord.Interaction):
#         reason_map = {
#             "dont-like": "内容が気に入らない(その他)",
#             "discord-violation": "Discordの各種規約違反",
#             "law-violation": "その他法令・規約違反",
#             "off-topic": "チャンネルの趣旨に合わない",
#             "harass": "誹謗中傷・差別・脅迫",
#             "negative-language": "強い言葉づかい・否定的表現",
#             "nsfw": "暴力的・エロ・グロ",
#             "spam": "荒らし・スパム",
#             "politics-religion": "政治・宗教的活動",
#             "exposing-information": "個人情報の過度な詮索・漏洩",
#             "mention": "無意味なメンション",
#             "inappropriate-profile": "不適切な名前・画像・鯖タグ",
#             "advertising-rule-violation": "宣伝ルール違反",
#             "question-rule-violation": "質問ルール違反",
#             "impersonation": "他参加者へのなりすまし"
#         }

#         reason = reason_map.get(self.values[0], "不明な理由")
#         important_logch = await self.bot.fetch_channel(config.channels.attention_report)
#         REPORTMESSAGE = f"""
# `通報内容:`{reason}
# `送信者　:`{self.message.author.mention}
# `ＵＲＬ　:`{self.message.jump_url}
# ### メッセージ内容
# {self.message.content if self.message.content else "メッセージ本文なし"}
# """
#         report_embed = discord.Embed(
#             title="通報を受け付けました",
#             description=REPORTMESSAGE,
#             color=0x80ff00
#         )
#         report_embed.set_image(url=self.message.attachments[0].url if self.message.attachments else None)
#         report_embed.set_author(name=interaction.user.display_name, icon_url=f"https://cdn.discordapp.com/embed/avatars/{random.randint(0, 5)}.png" if interaction.user.avatar is None else interaction.user.avatar.url)
#         report_embed.set_footer(text=f"通報ID: {self.custom_id}")

#         REPORTLOGMESSAGE = f"""
# `通報内容:`{reason}
# `送信日時:`{(self.message.created_at + timedelta(hours=9)).strftime('%Y/%m/%d %H:%M:%S')}
# `通報日時:`{datetime.now().strftime('%Y/%m/%d %H:%M:%S')}
# `通報者　:`{interaction.user.mention}/{interaction.user.id}
# `送信者　:`{self.message.author.mention}/{self.message.author.id}
# `ＵＲＬ　:`{self.message.jump_url}/{self.message.id}
# ### メッセージ内容
# {self.message.content if self.message.content else "メッセージ本文なし"}
# """
#         report_log_embed = discord.Embed(
#             title="通報がありました",
#             description=REPORTLOGMESSAGE,
#             color=0xff00ff
#         )
#         report_log_embed.set_image(url=self.message.attachments[0].url if self.message.attachments else None)
#         report_log_embed.set_footer(text=f"通報ID: {self.custom_id}")
#         await important_logch.send(embed=report_log_embed)
#         await interaction.response.edit_message(embed=report_embed, view=None)


class Fes_Expo_7th(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.context_menu = app_commands.ContextMenu(
            name="7th-Fes/EXPO-参加予定確認",
            callback=self.send_message
        )
        self.bot.tree.add_command(self.context_menu)

    async def send_message(self, interaction: discord.Interaction, message: discord.Message) -> None:
        targetdb = session3.query(Fes_Expo_7th_db).filter_by(userid=message.author.id).first()
        DESC = f"""7th-Fes/EXPO\n{message.author.mention}さんの参加予定確認
```
Fes Stage1: {"参加   〇" if targetdb.stage1 is True else "不参加 ✖"}
Fes Stage2: {"参加   〇" if targetdb.stage2 is True else "不参加 ✖"}
Fes Stage3: {"参加   〇" if targetdb.stage3 is True else "不参加 ✖"}
Fes Stage4: {"参加   〇" if targetdb.stage4 is True else "不参加 ✖"}
EXPO Day1 : {"参加   〇" if targetdb.day1 is True else "不参加 ✖"}
EXPO Day2 : {"参加   〇" if targetdb.day2 is True else "不参加 ✖"}
EXPO Day3 : {"参加   〇" if targetdb.day3 is True else "不参加 ✖"}
```
"""
        embed = discord.Embed(
            description=DESC,
            color=0x5EDEEC
        )
        if targetdb is None:
            await interaction.response.send_message(f"{message.author.display_name}さんの参加予定は登録されていません。", ephemeral=True)
            return
        await interaction.response.send_message(embed=embed, ephemeral=True, view=None)

    @app_commands.command(name="fes-expo-7th", description="参加予定登録・確認用コマンド")
    @app_commands.describe(
        choice="選択肢",
        target="登録/確認したい人",
        fes_stage1="Fes Stage1の参加予定(True=参加・False=不参加)",
        fes_stage2="Fes Stage2の参加予定(True=参加・False=不参加)",
        fes_stage3="Fes Stage3の参加予定(True=参加・False=不参加)",
        fes_stage4="Fes Stage4の参加予定(True=参加・False=不参加)",
        expo_day1="EXPO Day1の参加予定(True=参加・False=不参加)",
        expo_day2="EXPO Day2の参加予定(True=参加・False=不参加)",
        expo_day3="EXPO Day3の参加予定(True=参加・False=不参加)"
    )
    @app_commands.choices(
        choice=[
            app_commands.Choice(value="register", name="参加予定登録"),
            app_commands.Choice(value="edit", name="編集"),
            app_commands.Choice(value="list", name="一覧表示(自分にのみ表示)"),
            app_commands.Choice(value="list-open", name="一覧表示(全体に表示)")
        ]
    )
    async def fes_expo_7th(self, interaction: discord.Interaction, choice: app_commands.Choice[str], target: discord.Member, fes_stage1: bool = None, fes_stage2: bool = None, fes_stage3: bool = None, fes_stage4: bool = None, expo_day1: bool = None, expo_day2: bool = None, expo_day3: bool = None):

        if choice.value == "register":
            if interaction.user.guild_permissions.administrator is False and interaction.user.id != target.id:
                await interaction.response.send_message("他の人の参加予定を登録するには管理者権限が必要です。", ephemeral=True)
                return
            targetdb = session3.query(Fes_Expo_7th_db).filter_by(userid=target.id).first()
            if not targetdb:
                targetdb = Fes_Expo_7th_db(userid=target.id, username=target.display_name, stage1=fes_stage1 or False, stage2=fes_stage2 or False, stage3=fes_stage3 or False, stage4=fes_stage4 or False, day1=expo_day1 or False, day2=expo_day2 or False, day3=expo_day3 or False)
                session3.add(targetdb)
                session3.commit()
            await interaction.response.send_message(f"{target.display_name}さんの参加予定を登録しました。", ephemeral=True)

        elif choice.value == "edit":
            targetdb = session3.query(Fes_Expo_7th_db).filter_by(userid=target.id).first()
            if not targetdb:
                await interaction.response.send_message(f"{target.display_name}さんの参加予定は登録されていません。", ephemeral=True)
                return
            if fes_stage1 is not None:
                targetdb.stage1 = fes_stage1
            if fes_stage2 is not None:
                targetdb.stage2 = fes_stage2
            if fes_stage3 is not None:
                targetdb.stage3 = fes_stage3
            if fes_stage4 is not None:
                targetdb.stage4 = fes_stage4
            if expo_day1 is not None:
                targetdb.day1 = expo_day1
            if expo_day2 is not None:
                targetdb.day2 = expo_day2
            if expo_day3 is not None:
                targetdb.day3 = expo_day3
            session3.commit()
            await interaction.response.send_message(f"{target.display_name}さんの参加予定を更新しました。", ephemeral=True)

        elif choice.value == "list":
            targetdb = session3.query(Fes_Expo_7th_db).filter_by(userid=target.id).first()
            if not targetdb:
                await interaction.response.send_message(f"{target.display_name}さんの参加予定は登録されていません。", ephemeral=True)
                return
            DESC = f"""7th-Fes/EXPO\n{target.mention}さんの参加予定確認
```
Fes Stage1: {"参加   〇" if targetdb.stage1 is True else "不参加 ✖"}
Fes Stage2: {"参加   〇" if targetdb.stage2 is True else "不参加 ✖"}
Fes Stage3: {"参加   〇" if targetdb.stage3 is True else "不参加 ✖"}
Fes Stage4: {"参加   〇" if targetdb.stage4 is True else "不参加 ✖"}
EXPO Day1 : {"参加   〇" if targetdb.day1 is True else "不参加 ✖"}
EXPO Day2 : {"参加   〇" if targetdb.day2 is True else "不参加 ✖"}
EXPO Day3 : {"参加   〇" if targetdb.day3 is True else "不参加 ✖"}
```
"""
            embed = discord.Embed(
                description=DESC,
                color=0x5EDEEC
            )
            await interaction.response.send_message(embed=embed, ephemeral=True, view=None)

        elif choice.value == "list-open":
            targetdb = session3.query(Fes_Expo_7th_db).filter_by(userid=target.id).first()
            if not targetdb:
                await interaction.response.send_message(f"{target.display_name}さんの参加予定は登録されていません。", ephemeral=True)
                return
            DESC = f"""7th-Fes/EXPO\n{target.mention}さんの参加予定確認
```
Fes Stage1: {"参加   〇" if targetdb.stage1 is True else "不参加 ✖"}
Fes Stage2: {"参加   〇" if targetdb.stage2 is True else "不参加 ✖"}
Fes Stage3: {"参加   〇" if targetdb.stage3 is True else "不参加 ✖"}
Fes Stage4: {"参加   〇" if targetdb.stage4 is True else "不参加 ✖"}
EXPO Day1 : {"参加   〇" if targetdb.day1 is True else "不参加 ✖"}
EXPO Day2 : {"参加   〇" if targetdb.day2 is True else "不参加 ✖"}
EXPO Day3 : {"参加   〇" if targetdb.day3 is True else "不参加 ✖"}
```
"""
            embed = discord.Embed(
                description=DESC,
                color=0x5EDEEC
            )
            await interaction.response.send_message(embed=embed, view=None)


async def setup(bot: commands.Bot):
    await bot.add_cog(Fes_Expo_7th(bot))

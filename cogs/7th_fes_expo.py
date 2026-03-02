import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime

from config import config
from database import Fes_Expo_7th_db, session3


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
        interactionuserdb = session3.query(Fes_Expo_7th_db).filter_by(userid=interaction.user.id).first()
        if not interactionuserdb:
            await interaction.response.send_message("このシステムは鯖主の意向により廃止されました", ephemeral=True)
            return
        if targetdb is None:
            await interaction.response.send_message(f"{message.author.display_name}さんの参加予定は登録されていません。", ephemeral=True)
            return
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
        embed.set_footer(text="このシステムは鯖主の意向により廃止命令がされましたが、使ってくれている人も多くいるため、現在登録されている人のみ確認することができます。なのでこのコマンドに関しては口外厳禁です。")
        await interaction.response.send_message(embed=embed, ephemeral=True, view=None)
        print(f"[{datetime.now().strftime('%Y/%m/%d %H:%M:%S')}] {interaction.user.display_name} が {message.author.display_name} の参加予定を確認しました。")

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
            targetdb = session3.query(Fes_Expo_7th_db).filter_by(userid=target.id).first()
            if interaction.user.id != config.syunngiku_id:
                await interaction.response.send_message("このシステムは鯖主の意向により廃止されました", ephemeral=True)
                return
            if not targetdb:
                targetdb = Fes_Expo_7th_db(userid=target.id, username=target.display_name, stage1=fes_stage1 or False, stage2=fes_stage2 or False, stage3=fes_stage3 or False, stage4=fes_stage4 or False, day1=expo_day1 or False, day2=expo_day2 or False, day3=expo_day3 or False)
                session3.add(targetdb)
                session3.commit()
            await interaction.response.send_message(f"{target.display_name}さんの参加予定を登録しました。", ephemeral=True)

        elif choice.value == "edit":
            targetdb = session3.query(Fes_Expo_7th_db).filter_by(userid=target.id).first()
            if interaction.user.id != config.syunngiku_id:
                await interaction.response.send_message("このシステムは鯖主の意向により廃止されました", ephemeral=True)
                return
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
            interactionuserdb = session3.query(Fes_Expo_7th_db).filter_by(userid=interaction.user.id).first()
            if not interactionuserdb:
                await interaction.response.send_message("このシステムは鯖主の意向により廃止されました", ephemeral=True)
                return
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
            embed.set_footer(text="このシステムは鯖主の意向により廃止命令がされましたが、使ってくれている人も多くいるため、現在登録されている人のみ確認することができます。なのでこのコマンドに関しては口外厳禁です。")
            await interaction.response.send_message(embed=embed, ephemeral=True, view=None)
            print(f"[{datetime.now().strftime('%Y/%m/%d %H:%M:%S')}] {interaction.user.display_name} が {target.display_name} の参加予定を確認しました。")

        elif choice.value == "list-open":
            await interaction.response.send_message("このシステムは鯖主の意向により廃止されました", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(Fes_Expo_7th(bot))

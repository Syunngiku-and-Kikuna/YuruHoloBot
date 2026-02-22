import discord
from discord import app_commands
from discord.ext import commands

from database import Stickych, session


class Sticky(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        db = session.query(Stickych).filter_by(channelid=message.channel.id).first()
        if not db:
            return
        if db.messageid == 0:
            db.messageid = (await message.channel.send(db.text, silent=True)).id
            session.commit()
        msg = await message.channel.fetch_message(db.messageid)
        await msg.delete()
        db.messageid = (await message.channel.send(db.text, silent=True)).id
        session.commit()

    @app_commands.command(name="stickych", description="【運営用】固定メッセージチャンネルの設定)")
    @app_commands.describe(choice="選択肢", channel="変更するチャンネル", text="固定メッセージ内容")
    @app_commands.choices(
        choice=[
            app_commands.Choice(value="add", name="追加"),
            app_commands.Choice(value="remove", name="削除"),
            app_commands.Choice(value="edit", name="編集"),
            app_commands.Choice(value="list", name="チャンネル一覧")
        ]
    )
    async def setleveling(self, interaction: discord.Interaction, choice: app_commands.Choice[str], channel: discord.TextChannel, text: str = ""):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("このコマンドは管理者のみ使用できます。", ephemeral=True)
            return
        if choice.value == "add":
            if session.query(Stickych).filter_by(channelid=channel.id).first():
                await interaction.response.send_message("このチャンネルはすでに固定メッセージチャンネルに設定されています。", ephemeral=True)
                return
            new_db = Stickych(channelid=channel.id, channnelname=channel.name, text=text)
            session.add(new_db)
            session.commit()
            await interaction.response.send_message(f"{channel.mention}を固定メッセージチャンネルに追加しました。", ephemeral=True)
        elif choice.value == "remove":
            db = session.query(Stickych).filter_by(channelid=channel.id).first()
            if not db:
                await interaction.response.send_message("このチャンネルは固定メッセージチャンネルに設定されていません。", ephemeral=True)
                return
            session.delete(db)
            session.commit()
            await interaction.response.send_message(f"{channel.mention}を固定メッセージチャンネルから削除しました。", ephemeral=True)
        elif choice.value == "edit":
            db = session.query(Stickych).filter_by(channelid=channel.id).first()
            if not db:
                await interaction.response.send_message("このチャンネルは固定メッセージチャンネルに設定されていません。", ephemeral=True)
                return
            db.text = text
            session.commit()
            await interaction.response.send_message(f"{channel.mention}の固定メッセージ内容を更新しました。", ephemeral=True)
        elif choice.value == "list":
            dbs = session.query(Stickych).all()
            if not dbs:
                await interaction.response.send_message("現在、固定メッセージチャンネルは設定されていません。", ephemeral=True)
                return
            msg = "現在の固定メッセージチャンネル/メッセージ一覧:\n"
            for db in dbs:
                msg += f"## <#{db.channelid}>\n```{db.text}```\n"
            await interaction.response.send_message(msg, ephemeral=True)
        else:
            await interaction.response.send_message("無効な選択肢です。", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(Sticky(bot))

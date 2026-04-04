from discord import ButtonStyle, Interaction, app_commands
from discord.ext import commands
from discord.ui import Button, View, button

from config import config


class InviteButton(View):
    def __init__(self, bot: commands.Bot):
        super().__init__(timeout=None)
        self.bot = bot

    @button(label="02世代鯖に参加申請を送る", style=ButtonStyle.success, custom_id="gen02_invite_button")
    async def gen02invitebutton(self, interaction: Interaction, button: Button):
        ch = await self.bot.fetch_channel(config.channels.test_bot_ch1)
        await interaction.response.send_message("参加申請を送信しました。招待されるまで今しばらくお待ちください。", ephemeral=True)
        await ch.send(f"参加申請: {interaction.user.mention} ({interaction.user.name} / {interaction.user.id})")


class Gen02Invite(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="gen02", description="02世代鯖へ参加申請を送る")
    async def gen02invite(self, interaction: Interaction):
        view = InviteButton(self.bot)
        await interaction.response.send_message("02世代鯖へ参加申請を送りますか？\n送る場合は下のボタンを押してください。", view=view, ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(Gen02Invite(bot))
    bot.add_view(InviteButton(bot))

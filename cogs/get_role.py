import discord
from discord import app_commands
from discord.ext import commands


class GetRole(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="get_role", description="サーバー内の全ロールを取得します")
    async def get_role(self, interaction: discord.Interaction):
        for role in interaction.guild.roles:
            print(role.name)
        await interaction.response.send_message("サーバー内の全ロールをコンソールに出力しました。", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(GetRole(bot))

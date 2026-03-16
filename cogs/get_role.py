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

    @app_commands.command(name="create_role", description="ロールを作成します")
    async def create_role(self, interaction: discord.Interaction, role_name: str):
        if not role_name:
            await interaction.response.send_message("ロール名を指定してください。", ephemeral=True)
            return

        try:
            await interaction.guild.create_role(name=role_name, color=discord.Color.from_str("#5EDaab"))
            await interaction.response.send_message(f"ロール '{role_name}' を作成しました。", ephemeral=True)
        except discord.HTTPException as e:
            await interaction.response.send_message(f"ロールの作成に失敗しました: {e}", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(GetRole(bot))

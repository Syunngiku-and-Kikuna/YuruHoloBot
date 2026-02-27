import discord
from discord.ext import commands, tasks
from config import config
from datetime import datetime


class DayNotice(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.send_task.start()

    @tasks.loop(seconds=60)
    async def send_task(self):
        now = datetime.now()
        ch = await self.bot.fetch_channel(config.channels.expo_fes)
        DESCRIPTION = """開催まであとrest日"""
        countdown_embed = discord.Embed(
            title="hololive SUPER EXPO 2026\n&\nhololive 7th fes. Ridin’ on Dreams",
            description=DESCRIPTION,
            color=0x5EDEEC,
        )
        if now.hour == 0 and now.minute == 0:
            if now.date() == datetime(2026, 2, 28).date():
                countdown_embed.description = DESCRIPTION.replace("rest", "6")
                await ch.send(embed=countdown_embed)
            elif now.date() == datetime(2026, 3, 1).date():
                countdown_embed.description = DESCRIPTION.replace("rest", "5")
                await ch.send(embed=countdown_embed)
            elif now.date() == datetime(2026, 3, 2).date():
                countdown_embed.description = DESCRIPTION.replace("rest", "4")
                await ch.send(embed=countdown_embed)
            elif now.date() == datetime(2026, 3, 3).date():
                countdown_embed.description = DESCRIPTION.replace("rest", "3")
                await ch.send(embed=countdown_embed)
            elif now.date() == datetime(2026, 3, 4).date():
                countdown_embed.description = DESCRIPTION.replace("rest", "2")
                await ch.send(embed=countdown_embed)
            elif now.date() == datetime(2026, 3, 5).date():
                countdown_embed.description = DESCRIPTION.replace("rest", "1")
                await ch.send(embed=countdown_embed)
            elif now.date() == datetime(2026, 3, 6).date():
                countdown_embed.description = "# EXPO Day1\n&\n# Fes Stage1\n# 本日開催!!"
                await ch.send(embed=countdown_embed)
            elif now.date() == datetime(2026, 3, 7).date():
                countdown_embed.description = "# EXPO Day2\n&\n# Fes Stage2/3\n# 本日開催!!"
                await ch.send(embed=countdown_embed)
            elif now.date() == datetime(2026, 3, 8).date():
                countdown_embed.description = "# EXPO Day3\n&\n# Fes Stage4\n# 本日開催!!"
                await ch.send(embed=countdown_embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(DayNotice(bot))

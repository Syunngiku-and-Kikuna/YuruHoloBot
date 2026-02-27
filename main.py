import discord
import asyncio
from os import listdir
from discord.ext import commands
from datetime import datetime

from config import config


class MyBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def setup_hook(self) -> None:
        for name in listdir("cogs"):
            if name.endswith(".py") and not name.startswith("_"):
                f = f"cogs.{name.replace('.py', '')}"
                await self.load_extension(f)
                print(f"[{datetime.now().strftime('%Y/%m/%d %H:%M:%S')}] 「{f}」が正常にロードされました.")

    async def on_ready(self):
        print(f"[{datetime.now().strftime('%Y/%m/%d %H:%M:%S')}] ログインしました")
        await self.load_extension("jishaku")
        await self.tree.sync()

    async def start(self, token: str) -> None:
        return await super().start(token)

    async def close(self) -> None:
        for e in list(self.extensions.keys()):
            await self.unload_extension(e)
        print("all exts unloaded.")
        return await super().close()


if __name__ == "__main__":
    intents = discord.Intents.all()
    bot = MyBot(command_prefix="sy!", intents=intents)
    asyncio.run(bot.start(config.token))


import os
from pathlib import Path

import discord as dc
from discord.ext import commands
from dotenv import load_dotenv
import aiohttp

from APIs.wynnapi import WynnAPI


BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

TOKEN = os.getenv("DISCORD_TOKEN")
WYNN_TOKEN = os.getenv("WYNN_TOKEN")


COGS = [
    "commands.fun",
    "commands.wynncraft",
    "commands.mightyai",
]


class MightyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=None,
            intents=dc.Intents.all()
        )
    async def setup_hook(self):
        # Connect to Wynncraft API
        self.api = await WynnAPI.api()
        print("Wynncraft API initialized!")

        # Load cogs
        for extension in COGS:
            await self.load_extension(extension)
            print(f"Loaded: {extension}")

        # Sync slash commands

        synced = await self.tree.sync()
        print(f"Synced {len(synced)} commands.")

    async def on_ready(self):
        print(f"Logged in as {self.user}")
        print("MightyBot is online!")

    async def close(self):
        if hasattr(self, 'api') and self.api:
            await self.api.close()

        await super().close()


bot = MightyBot()

if __name__ == "__main__":
    bot.run(TOKEN)


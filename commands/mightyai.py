import aiohttp
import asyncio

import discord as dc
from discord.ext import commands
from discord import app_commands

from APIs.mightybotai import ask_mighty


class mightyai(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="ask",
        description="Ask MightyBot a question"
    )
    async def ask(self, interaction: dc.Interaction, question: str):

        await interaction.response.defer(thinking=True)

        try:
            answer = await ask_mighty(question)

            if not answer:
                answer = "Your prompt crashed my pi."

            await interaction.followup.send(
                answer[:1900],
                allowed_mentions=dc.AllowedMentions.none()
            )

        except (aiohttp.ClientError, asyncio.TimeoutError) as e:

            print(
                f"MightyBot failed. Also: {type(e).__name__}: {e}"
            )

            await interaction.followup.send(
                f"MightyBot failed you. Also: {type(e).__name__}: {e}"
            )

        except Exception as e:

            print(
                f"TinyLlama error: {type(e).__name__}: {e}"
            )

            await interaction.followup.send(
                f"This happened: {type(e).__name__}: {e}"
            )


async def setup(bot):
    await bot.add_cog(mightyai(bot))


import discord as dc

from discord.ext import commands
from discord import app_commands

# fun
import random as rnd


class fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="roll", description="roll some dice")
    async def roll(
        self,
        interaction: dc.Interaction,
        amount: app_commands.Range[int, 1, 1000],
        dice_type: app_commands.Range[int, 2, 100],
        modifier: int = 0
    ):

        grand_result = 0
        numbers = []
        number_write = ''

        for i in range(amount):
            result = rnd.randint(1, dice_type)
            numbers.append(result)
            grand_result += result

        grand_result += modifier

        for number in numbers:
            number_write += f'{number} + '

        await interaction.response.send_message(
            f'{amount}d{dice_type} + {modifier}\n'
            f'Rolls: {number_write}\n'
            f'Total: {grand_result}\n'
            'That seems like a roll.'
        )

    @app_commands.command(
        name="joe",
        description="who is joe?"
    )
    async def joe(self, interaction: dc.Interaction):

        await interaction.response.send_message("JOE MAMA!")

    @app_commands.command(
        name="coinflip",
        description="flips a coin"
    )
    async def coinflip(self, interaction: dc.Interaction):

        if rnd.randint(1, 2) == 1:
            await interaction.response.send_message('Heads!')
            return

        await interaction.response.send_message('Tails!')


async def setup(bot):
    await bot.add_cog(fun(bot))
